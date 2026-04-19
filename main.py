"""
Main application file for Mercari Auto Price Down
"""

import logging
import sys
import os
from dotenv import load_dotenv
import config
from scheduler import PriceReduceScheduler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main function"""
    
    # Get credentials from environment variables
    email = os.getenv('MERCARI_EMAIL')
    password = os.getenv('MERCARI_PASSWORD')
    
    if not email or not password:
        logger.error('Please set MERCARI_EMAIL and MERCARI_PASSWORD in .env file')
        sys.exit(1)
    
    logger.info('Starting Mercari Auto Price Down App')
    
    try:
        # Initialize scheduler
        scheduler = PriceReduceScheduler(email, password)
        
        # Start scheduler
        if scheduler.start():
            logger.info('Scheduler is running. Press Ctrl+C to stop.')
            
            # Keep the application running
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info('Stopping scheduler...')
                scheduler.stop()
                logger.info('Application stopped')
        else:
            logger.error('Failed to start scheduler')
            sys.exit(1)
            
    except Exception as e:
        logger.error(f'Error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
