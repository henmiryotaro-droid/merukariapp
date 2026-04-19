"""
Scheduler module for automatic price reduction
"""

import logging
import sqlite3
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
import config
from mercari import MercariBot

logger = logging.getLogger(__name__)

# Database for tracking items
class ItemDB:
    def __init__(self, db_file):
        self.db_file = db_file
        self._init_db()
    
    def _init_db(self):
        """Initialize database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY,
                item_id TEXT UNIQUE NOT NULL,
                last_price_down TIMESTAMP,
                current_price INTEGER,
                min_price INTEGER DEFAULT 100,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_item(self, item_id, current_price, min_price=100):
        """Add item to track"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO items (id, item_id, current_price, min_price)
                VALUES (?, ?, ?, ?)
            ''', (item_id, item_id, current_price, min_price))
            conn.commit()
            conn.close()
            logger.info(f'Added item {item_id} to tracking')
            return True
        except Exception as e:
            logger.error(f'Error adding item: {e}')
            return False
    
    def get_tracked_items(self):
        """Get all tracked items"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT item_id FROM items')
            items = [row[0] for row in cursor.fetchall()]
            conn.close()
            return items
        except Exception as e:
            logger.error(f'Error getting tracked items: {e}')
            return []
    
    def should_reduce_price(self, item_id):
        """Check if item should have price reduced today"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT last_price_down FROM items WHERE item_id = ?
            ''', (item_id,))
            result = cursor.fetchone()
            conn.close()
            
            if not result or result[0] is None:
                return True
            
            last_reduction = datetime.fromisoformat(result[0])
            now = datetime.now()
            
            # Check if 24 hours have passed
            return (now - last_reduction).total_seconds() >= 86400
        except Exception as e:
            logger.error(f'Error checking reduction time: {e}')
            return False
    
    def update_price_down(self, item_id, new_price):
        """Update last price down time"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE items 
                SET last_price_down = ?, current_price = ?
                WHERE item_id = ?
            ''', (datetime.now().isoformat(), new_price, item_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f'Error updating price down time: {e}')
            return False


class PriceReduceScheduler:
    """Scheduler for automatic price reduction"""
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.scheduler = None
        self.bot = None
        self.db = ItemDB(config.DB_FILE)
        
    def init_scheduler(self):
        """Initialize APScheduler"""
        jobstores = {
            'default': SQLAlchemyJobStore(url=f'sqlite:///{config.SCHEDULER_DB_FILE}')
        }
        executors = {
            'default': ThreadPoolExecutor(max_workers=1)
        }
        
        self.scheduler = BackgroundScheduler(
            jobstores=jobstores,
            executors=executors,
            timezone='Asia/Tokyo'
        )
        
    def start(self):
        """Start scheduler"""
        try:
            self.init_scheduler()
            
            # Add daily job at 21:00 (9:00 PM)
            self.scheduler.add_job(
                self.run_price_reduction,
                'cron',
                hour=21,
                minute=0,
                id='daily_price_reduction',
                name='Daily Price Reduction',
                replace_existing=True
            )
            
            self.scheduler.start()
            logger.info('Scheduler started')
            return True
        except Exception as e:
            logger.error(f'Error starting scheduler: {e}')
            return False
    
    def run_price_reduction(self):
        """Run price reduction task"""
        try:
            logger.info('Starting price reduction task...')
            self.bot = MercariBot(self.email, self.password)
            
            if not self.bot.login():
                logger.error('Failed to login')
                return
            
            items = self.bot.get_selling_items()
            
            for item in items:
                item_id = item['id']
                
                if self.db.should_reduce_price(item_id):
                    if self.bot.reduce_price(item_id, config.PRICE_DOWN_AMOUNT):
                        # Update database with new price
                        self.db.update_price_down(item_id, None)
                else:
                    logger.info(f'Item {item_id} already reduced today')
            
            logger.info('Price reduction task completed')
            
        except Exception as e:
            logger.error(f'Error in price reduction task: {e}')
        finally:
            if self.bot:
                self.bot.close()
    
    def add_item_to_track(self, item_id, current_price, min_price=100):
        """Add item to track"""
        return self.db.add_item(item_id, current_price, min_price)
    
    def get_tracked_items(self):
        """Get tracked items"""
        return self.db.get_tracked_items()
    
    def stop(self):
        """Stop scheduler"""
        if self.scheduler:
            self.scheduler.shutdown()
            logger.info('Scheduler stopped')
