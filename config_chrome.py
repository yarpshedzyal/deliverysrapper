# config.py

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to the ChromeDriver executable
CHROMEDRIVER_PATH = 'chromedriver-win64\chromedriver.exe'

# Chrome options
CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_argument('--headless')  # Run in headless mode
CHROME_OPTIONS.add_argument('--disable-gpu')
CHROME_OPTIONS.add_argument('--window-size=1920,1080')
CHROME_OPTIONS.add_argument('--no-sandbox')
CHROME_OPTIONS.add_argument('--disable-dev-shm-usage')
CHROME_OPTIONS.add_argument('--log-level=3')  # Suppress console messages


# Chrome service
CHROME_SERVICE = Service(CHROMEDRIVER_PATH)
