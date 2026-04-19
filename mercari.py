"""
Mercari integration module using Selenium
"""

import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)


class MercariBot:
    """Bot to automate Mercari price reduction"""
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        self.wait = None
        
    def _init_driver(self):
        """Initialize Chrome WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def login(self):
        """Login to Mercari"""
        try:
            self._init_driver()
            logger.info('Logging in to Mercari...')
            
            # Navigate to Mercari
            self.driver.get('https://www.mercari.com/jp/mypage/items/')
            time.sleep(2)
            
            # Click on login link if necessary
            try:
                # Try to find and click login button
                login_button = self.driver.find_element(By.XPATH, '//a[contains(text(), "ログイン")]')
                login_button.click()
                time.sleep(2)
            except NoSuchElementException:
                logger.info('Already on login page or logged in')
            
            # Enter email
            email_input = self.wait.until(
                EC.presence_of_element_located((By.ID, 'email'))
            )
            email_input.send_keys(self.email)
            time.sleep(0.5)
            
            # Enter password
            password_input = self.driver.find_element(By.ID, 'password')
            password_input.send_keys(self.password)
            time.sleep(0.5)
            
            # Click login button
            login_btn = self.driver.find_element(By.XPATH, '//button[contains(text(), "ログイン")]')
            login_btn.click()
            
            # Wait for redirect to user page
            self.wait.until(EC.url_contains('mypage'))
            logger.info('Successfully logged in')
            return True
            
        except TimeoutException:
            logger.error('Login timeout')
            return False
        except Exception as e:
            logger.error(f'Login error: {e}')
            return False
    
    def get_selling_items(self):
        """Get list of items currently being sold"""
        try:
            logger.info('Fetching selling items...')
            
            # Navigate to selling items page
            self.driver.get('https://www.mercari.com/jp/mypage/items/')
            time.sleep(2)
            
            items = []
            
            # Get all item listings
            item_elements = self.driver.find_elements(
                By.XPATH, 
                '//a[contains(@href, "/item/")]'
            )
            
            for item_el in item_elements:
                try:
                    item_url = item_el.get_attribute('href')
                    if item_url and 'item' in item_url:
                        items.append({
                            'url': item_url,
                            'id': item_url.split('/')[-1]
                        })
                except:
                    continue
            
            logger.info(f'Found {len(items)} selling items')
            return items
            
        except Exception as e:
            logger.error(f'Error fetching items: {e}')
            return []
    
    def reduce_price(self, item_id, reduce_amount=100):
        """Reduce price of an item by specified amount"""
        try:
            logger.info(f'Reducing price for item {item_id}...')
            
            # Navigate to item edit page
            item_url = f'https://www.mercari.com/jp/items/{item_id}/edit/'
            self.driver.get(item_url)
            time.sleep(2)
            
            # Find current price
            price_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, 'price'))
            )
            current_price = int(price_input.get_attribute('value'))
            new_price = max(current_price - reduce_amount, 100)  # Minimum 100 yen
            
            # Clear and enter new price
            price_input.clear()
            price_input.send_keys(str(new_price))
            time.sleep(0.5)
            
            # Find and click save button
            save_button = self.driver.find_element(
                By.XPATH, 
                '//button[contains(text(), "保存")]'
            )
            save_button.click()
            
            # Wait for success
            time.sleep(2)
            logger.info(f'Successfully reduced price from {current_price} to {new_price}')
            return True
            
        except Exception as e:
            logger.error(f'Error reducing price for {item_id}: {e}')
            return False
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info('WebDriver closed')
