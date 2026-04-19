#!/usr/bin/env python3
"""
Setup script for Mercari Auto Price Down App
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print('Error: Python 3.8 or higher is required')
        sys.exit(1)
    print(f'✓ Python {sys.version.split()[0]} detected')


def check_chrome():
    """Check if Chrome/Chromium is installed"""
    try:
        result = subprocess.run(
            ['which', 'google-chrome'] or ['which', 'chromium'] or ['which', 'chromium-browser'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print('✓ Chrome detected')
            return True
    except:
        pass
    
    print('⚠ Chrome/Chromium not found in PATH')
    print('  Install Chrome: https://www.google.com/chrome/')
    return False


def check_chromedriver():
    """Check if Chromedriver is installed"""
    try:
        result = subprocess.run(
            ['which', 'chromedriver'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print('✓ Chromedriver detected')
            return True
    except:
        pass
    
    print('⚠ Chromedriver not found in PATH')
    print('  Install Chromedriver:')
    print('    macOS: brew install chromedriver')
    print('    Or download from: https://chromedriver.chromium.org/')
    return False


def install_dependencies():
    """Install Python dependencies"""
    print('\nInstalling Python dependencies...')
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print('✓ Dependencies installed')
        return True
    except subprocess.CalledProcessError:
        print('✗ Failed to install dependencies')
        return False


def create_env_file():
    """Create .env file from template"""
    if os.path.exists('.env'):
        print('✓ .env file already exists')
        return True
    
    if not os.path.exists('.env.example'):
        print('✗ .env.example not found')
        return False
    
    try:
        with open('.env.example', 'r') as f:
            content = f.read()
        
        with open('.env', 'w') as f:
            f.write(content)
        
        print('✓ .env file created from template')
        print('  Please edit .env with your Mercari credentials')
        return True
    except Exception as e:
        print(f'✗ Error creating .env file: {e}')
        return False


def run_tests():
    """Run tests"""
    print('\nRunning tests...')
    
    try:
        result = subprocess.run(
            [sys.executable, 'test_app.py'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print('✓ All tests passed')
            return True
        else:
            print('✗ Some tests failed')
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f'✗ Error running tests: {e}')
        return False


def main():
    """Main setup function"""
    print('=' * 50)
    print('Mercari Auto Price Down App - Setup')
    print('=' * 50)
    
    # Check Python version
    check_python_version()
    
    # Check dependencies
    print('\nChecking system dependencies...')
    has_chrome = check_chrome()
    has_chromedriver = check_chromedriver()
    
    if not (has_chrome and has_chromedriver):
        print('\n⚠ Please install the missing dependencies')
        print('  Windows/Mac: https://www.google.com/chrome/')
        print('  Chromedriver: https://chromedriver.chromium.org/')
    
    # Install Python dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print('⚠ Failed to create .env file, please do it manually')
    
    # Run tests
    if not run_tests():
        print('\n⚠ Some tests failed, but you may continue')
    
    # Setup complete
    print('\n' + '=' * 50)
    print('Setup complete!')
    print('=' * 50)
    print('\nNext steps:')
    print('1. Edit .env with your Mercari credentials')
    print('2. Run: python main.py')
    print('\nFor CLI commands, run: python cli.py --help')
    print('=' * 50)


if __name__ == '__main__':
    main()
