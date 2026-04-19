"""
Configuration file for Mercari Auto Price Down App
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Email and password for Mercari
MERCARI_EMAIL = os.getenv('MERCARI_EMAIL', '')
MERCARI_PASSWORD = os.getenv('MERCARI_PASSWORD', '')

# Price down settings
PRICE_DOWN_AMOUNT = 100  # 100 yen
PRICE_DOWN_INTERVAL = 24 * 60 * 60  # 24 hours in seconds

# Chrome driver settings
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH', '/opt/homebrew/bin/chromedriver')

# Database settings
DB_FILE = BASE_DIR / 'mercari_items.db'

# Log settings
LOG_LEVEL = 'INFO'
LOG_FILE = BASE_DIR / 'app.log'

# Scheduler settings
SCHEDULER_JOB_STORE = 'sqlite'
SCHEDULER_DB_FILE = BASE_DIR / 'scheduler.db'
