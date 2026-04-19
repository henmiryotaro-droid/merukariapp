"""
Test script for Mercari Auto Price Down App
"""

import unittest
import os
import tempfile
from pathlib import Path
from scheduler import ItemDB


class TestItemDB(unittest.TestCase):
    """Test ItemDB functionality"""
    
    def setUp(self):
        """Set up test database"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        self.db = ItemDB(self.test_db.name)
    
    def tearDown(self):
        """Clean up test database"""
        if os.path.exists(self.test_db.name):
            os.remove(self.test_db.name)
    
    def test_add_item(self):
        """Test adding item to database"""
        result = self.db.add_item('test_item_001', 5000, 100)
        self.assertTrue(result)
        
        items = self.db.get_tracked_items()
        self.assertIn('test_item_001', items)
    
    def test_get_tracked_items(self):
        """Test getting tracked items"""
        self.db.add_item('item_1', 1000)
        self.db.add_item('item_2', 2000)
        
        items = self.db.get_tracked_items()
        self.assertEqual(len(items), 2)
        self.assertIn('item_1', items)
        self.assertIn('item_2', items)
    
    def test_should_reduce_price_new_item(self):
        """Test price reduction check for new item"""
        self.db.add_item('new_item', 3000)
        result = self.db.should_reduce_price('new_item')
        self.assertTrue(result)
    
    def test_update_price_down(self):
        """Test updating price down time"""
        self.db.add_item('update_test', 4000)
        result = self.db.update_price_down('update_test', 3900)
        self.assertTrue(result)


class TestConfig(unittest.TestCase):
    """Test configuration"""
    
    def test_config_values(self):
        """Test that config values are set correctly"""
        import config
        
        self.assertEqual(config.PRICE_DOWN_AMOUNT, 100)
        self.assertIsNotNone(config.BASE_DIR)
        self.assertTrue(config.DB_FILE.parent.exists())


class TestMercariBot(unittest.TestCase):
    """Test MercariBot (without actual login)"""
    
    def test_mercari_bot_init(self):
        """Test MercariBot initialization"""
        from mercari import MercariBot
        
        bot = MercariBot('test@example.com', 'password')
        self.assertEqual(bot.email, 'test@example.com')
        self.assertEqual(bot.password, 'password')
        self.assertIsNone(bot.driver)


def run_tests():
    """Run all tests"""
    print('Running tests...')
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestItemDB))
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestMercariBot))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    import sys
    sys.exit(run_tests())
