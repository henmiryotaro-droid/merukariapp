"""
Advanced configuration and management for Mercari Auto Price Down App
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class ItemConfig:
    """Configuration for individual items"""
    
    def __init__(
        self,
        item_id: str,
        daily_reduction: int = 100,
        min_price: int = 100,
        max_reductions: Optional[int] = None,
        enabled: bool = True,
        notes: str = ''
    ):
        self.item_id = item_id
        self.daily_reduction = daily_reduction
        self.min_price = min_price
        self.max_reductions = max_reductions  # None = unlimited
        self.enabled = enabled
        self.notes = notes
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'item_id': self.item_id,
            'daily_reduction': self.daily_reduction,
            'min_price': self.min_price,
            'max_reductions': self.max_reductions,
            'enabled': self.enabled,
            'notes': self.notes
        }
    
    @staticmethod
    def from_dict(data: Dict):
        """Create from dictionary"""
        return ItemConfig(
            item_id=data['item_id'],
            daily_reduction=data.get('daily_reduction', 100),
            min_price=data.get('min_price', 100),
            max_reductions=data.get('max_reductions'),
            enabled=data.get('enabled', True),
            notes=data.get('notes', '')
        )


class ScheduleConfig:
    """Configuration for scheduler"""
    
    def __init__(
        self,
        hour: int = 9,
        minute: int = 0,
        timezone: str = 'Asia/Tokyo',
        enabled: bool = True
    ):
        self.hour = hour
        self.minute = minute
        self.timezone = timezone
        self.enabled = enabled
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'hour': self.hour,
            'minute': self.minute,
            'timezone': self.timezone,
            'enabled': self.enabled
        }
    
    @staticmethod
    def from_dict(data: Dict):
        """Create from dictionary"""
        return ScheduleConfig(
            hour=data.get('hour', 9),
            minute=data.get('minute', 0),
            timezone=data.get('timezone', 'Asia/Tokyo'),
            enabled=data.get('enabled', True)
        )


class AppConfig:
    """Main application configuration"""
    
    def __init__(self, config_file: str = 'items_config.json'):
        self.config_file = Path(config_file)
        self.items: Dict[str, ItemConfig] = {}
        self.schedule = ScheduleConfig()
        self.settings = {
            'log_level': 'INFO',
            'headless_mode': False,  # Run browser in headless mode
            'debug_mode': False
        }
        self.load()
    
    def load(self):
        """Load configuration from file"""
        if not self.config_file.exists():
            logger.info(f'Config file {self.config_file} not found, using defaults')
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load schedule config
            if 'schedule' in data:
                self.schedule = ScheduleConfig.from_dict(data['schedule'])
            
            # Load items
            if 'items' in data:
                for item_data in data['items']:
                    item = ItemConfig.from_dict(item_data)
                    self.items[item.item_id] = item
            
            # Load settings
            if 'settings' in data:
                self.settings.update(data['settings'])
            
            logger.info(f'Loaded config from {self.config_file}')
            
        except json.JSONDecodeError as e:
            logger.error(f'Invalid JSON in {self.config_file}: {e}')
        except Exception as e:
            logger.error(f'Error loading config: {e}')
    
    def save(self):
        """Save configuration to file"""
        try:
            data = {
                'schedule': self.schedule.to_dict(),
                'items': [item.to_dict() for item in self.items.values()],
                'settings': self.settings
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f'Saved config to {self.config_file}')
            return True
            
        except Exception as e:
            logger.error(f'Error saving config: {e}')
            return False
    
    def add_item(self, item_config: ItemConfig):
        """Add item to configuration"""
        self.items[item_config.item_id] = item_config
        logger.info(f'Added item {item_config.item_id}')
    
    def remove_item(self, item_id: str):
        """Remove item from configuration"""
        if item_id in self.items:
            del self.items[item_id]
            logger.info(f'Removed item {item_id}')
            return True
        return False
    
    def get_item(self, item_id: str) -> Optional[ItemConfig]:
        """Get item configuration"""
        return self.items.get(item_id)
    
    def get_enabled_items(self) -> List[ItemConfig]:
        """Get all enabled items"""
        return [item for item in self.items.values() if item.enabled]
    
    def enable_item(self, item_id: str):
        """Enable an item"""
        if item_id in self.items:
            self.items[item_id].enabled = True
            logger.info(f'Enabled item {item_id}')
            return True
        return False
    
    def disable_item(self, item_id: str):
        """Disable an item"""
        if item_id in self.items:
            self.items[item_id].enabled = False
            logger.info(f'Disabled item {item_id}')
            return True
        return False
    
    def set_schedule(self, hour: int, minute: int):
        """Update schedule"""
        self.schedule.hour = hour
        self.schedule.minute = minute
        logger.info(f'Schedule set to {hour:02d}:{minute:02d}')
    
    def print_summary(self):
        """Print configuration summary"""
        print('\n' + '=' * 50)
        print('Application Configuration Summary')
        print('=' * 50)
        
        print(f'\nSchedule: {self.schedule.hour:02d}:{self.schedule.minute:02d} ({self.schedule.timezone})')
        print(f'Enabled: {self.schedule.enabled}')
        
        print(f'\nTracked Items: {len(self.items)}')
        enabled_count = len(self.get_enabled_items())
        print(f'Enabled: {enabled_count}')
        
        if self.items:
            print('\nItems:')
            for item in self.items.values():
                status = '✓' if item.enabled else '✗'
                print(f'  [{status}] {item.item_id}')
                print(f'      Daily: ¥{item.daily_reduction}, Min: ¥{item.min_price}')
                if item.notes:
                    print(f'      Notes: {item.notes}')
        
        print('\n' + '=' * 50)


def create_example_config():
    """Create example configuration file"""
    config = AppConfig('items_config_example.json')
    
    # Add example items
    item1 = ItemConfig(
        item_id='m123456789012345678',
        daily_reduction=100,
        min_price=500,
        max_reductions=20,
        notes='Example item 1'
    )
    
    item2 = ItemConfig(
        item_id='m987654321098765432',
        daily_reduction=200,
        min_price=1000,
        enabled=True,
        notes='Example item 2 - Higher reduction'
    )
    
    config.add_item(item1)
    config.add_item(item2)
    
    # Update settings
    config.settings['log_level'] = 'DEBUG'
    config.settings['headless_mode'] = True
    
    # Save
    config.save()
    config.print_summary()


if __name__ == '__main__':
    print('Advanced Configuration Module')
    print('Creating example configuration...\n')
    create_example_config()
