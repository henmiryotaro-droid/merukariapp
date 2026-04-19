"""
CLI commands for Mercari Auto Price Down App
"""

import argparse
import logging
import sys
from mercari import MercariBot
from scheduler import PriceReduceScheduler, ItemDB
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_login(email, password):
    """Test login to Mercari"""
    logger.info('Testing login...')
    bot = MercariBot(email, password)
    
    try:
        if bot.login():
            logger.info('✓ Login successful')
            bot.close()
            return True
        else:
            logger.error('✗ Login failed')
            return False
    except Exception as e:
        logger.error(f'✗ Login error: {e}')
        return False


def list_items(email, password):
    """List all selling items"""
    logger.info('Fetching selling items...')
    bot = MercariBot(email, password)
    
    try:
        if not bot.login():
            logger.error('Login failed')
            return False
        
        items = bot.get_selling_items()
        
        if items:
            logger.info(f'Found {len(items)} selling items:')
            for i, item in enumerate(items, 1):
                logger.info(f'  {i}. ID: {item["id"]} - {item["url"]}')
        else:
            logger.info('No selling items found')
        
        bot.close()
        return True
        
    except Exception as e:
        logger.error(f'Error listing items: {e}')
        return False


def reduce_price_manual(email, password, item_id, amount=100):
    """Manually reduce price of an item"""
    logger.info(f'Reducing price for item {item_id} by {amount}yen...')
    bot = MercariBot(email, password)
    
    try:
        if not bot.login():
            logger.error('Login failed')
            return False
        
        if bot.reduce_price(item_id, amount):
            logger.info(f'✓ Price reduced successfully')
            # Update database
            db = ItemDB(config.DB_FILE)
            db.update_price_down(item_id, None)
            bot.close()
            return True
        else:
            logger.error('✗ Failed to reduce price')
            bot.close()
            return False
            
    except Exception as e:
        logger.error(f'Error reducing price: {e}')
        return False


def track_item(item_id, current_price, min_price=100):
    """Add item to tracking"""
    logger.info(f'Adding item {item_id} to tracking...')
    db = ItemDB(config.DB_FILE)
    
    if db.add_item(item_id, current_price, min_price):
        logger.info('✓ Item added to tracking')
        return True
    else:
        logger.error('✗ Failed to add item')
        return False


def list_tracked_items():
    """List all tracked items"""
    db = ItemDB(config.DB_FILE)
    items = db.get_tracked_items()
    
    if items:
        logger.info(f'Tracked items ({len(items)}):')
        for item in items:
            logger.info(f'  - {item}')
    else:
        logger.info('No tracked items')
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Mercari Auto Price Down CLI'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Test login command
    login_parser = subparsers.add_parser('login', help='Test login to Mercari')
    login_parser.add_argument('email', help='Mercari email')
    login_parser.add_argument('password', help='Mercari password')
    
    # List items command
    list_parser = subparsers.add_parser('list', help='List all selling items')
    list_parser.add_argument('email', help='Mercari email')
    list_parser.add_argument('password', help='Mercari password')
    
    # Reduce price command
    reduce_parser = subparsers.add_parser('reduce', help='Reduce price of an item')
    reduce_parser.add_argument('email', help='Mercari email')
    reduce_parser.add_argument('password', help='Mercari password')
    reduce_parser.add_argument('item_id', help='Item ID')
    reduce_parser.add_argument(
        '--amount', 
        type=int, 
        default=100, 
        help='Amount to reduce (default: 100)'
    )
    
    # Track item command
    track_parser = subparsers.add_parser('track', help='Add item to tracking')
    track_parser.add_argument('item_id', help='Item ID')
    track_parser.add_argument(
        '--price', 
        type=int, 
        required=True, 
        help='Current price'
    )
    track_parser.add_argument(
        '--min-price', 
        type=int, 
        default=100, 
        help='Minimum price (default: 100)'
    )
    
    # List tracked command
    subparsers.add_parser('tracked', help='List tracked items')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'login':
        success = test_login(args.email, args.password)
    elif args.command == 'list':
        success = list_items(args.email, args.password)
    elif args.command == 'reduce':
        success = reduce_price_manual(
            args.email, 
            args.password, 
            args.item_id, 
            args.amount
        )
    elif args.command == 'track':
        success = track_item(args.item_id, args.price, args.min_price)
    elif args.command == 'tracked':
        success = list_tracked_items()
    else:
        parser.print_help()
        sys.exit(1)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
