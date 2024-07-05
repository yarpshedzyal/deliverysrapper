from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config_chrome import CHROME_OPTIONS, CHROME_SERVICE
import re
import time
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("scrap_status_thestore.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_driver():
    logger.info("Initializing the WebDriver.")
    driver = webdriver.Chrome(service=CHROME_SERVICE, options=CHROME_OPTIONS)
    return driver

def extract_status(text):
    pattern = r'<span class="[^"]*order-status[^"]*">\s*(.*?)\s*</span>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return 'Unknown'

def scrap_status_thestore(the_store_set: set):
    driver = create_driver()
    result_the_store = {}
    number_of_orders = len(the_store_set)
    counter_for_done = 0
    screenshots = []

    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')

    for order_id in the_store_set:
        try:
            logger.info(f"Processing order ID: {order_id}")
            driver.get('https://www.therestaurantstore.com/login')

            # Wait for the email field to be present
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'order-email'))
            )
            order_number_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'order-number'))
            )

            email_field.send_keys('alina.troian.proton@gmail.com')
            order_number_field.send_keys(str(order_id))

            # Wait for the submit button to be clickable
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#track-orders-form > div > div > div > button'))
            )
            submit_button.click()

            # Verify if the current page is the order status page
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#main > div:nth-child(4) > div > div:nth-child(1) > div > div > div.w-full.xl\:w-72.lg\:mr-6.xl\:mr-12 > div > ul:nth-child(1) > li:nth-child(3)'))
            )

            # Extraction of status info
            status_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#main > div:nth-child(4) > div > div:nth-child(1) > div > div > div.w-full.xl\:w-72.lg\:mr-6.xl\:mr-12 > div > ul:nth-child(1) > li:nth-child(3)'))
            )
            status_html = status_element.get_attribute('outerHTML')
            status_info = extract_status(status_html)

            # Classification of orders
            if status_info == 'Shipped':
                table = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#simple-tracking-details > div > div > table > tbody'))
                )
                rows = table.find_elements(By.TAG_NAME, 'tr')
                table_data = []
                for row in rows:
                    date = row.find_element(By.CSS_SELECTOR, 'td:nth-child(1) span').text.strip()
                    carrier = row.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text.strip()
                    tracking_number = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text.strip()
                    tracking_link = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4) a').get_attribute('href')

                    table_data.append({
                        'Date': date,
                        'Carrier': carrier,
                        'Tracking Number': tracking_number,
                        'Tracking Link': tracking_link
                    })
            elif status_info == 'Processing':
                table_data = 'None'

            result_the_store[order_id] = [status_info, table_data]

        except Exception as e:
            logger.error(f"An error occurred for order ID {order_id}: {e}")
            screenshot_path = f"screenshots/order_{order_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(screenshot_path)
            logger.error(f"Screenshot saved to {screenshot_path}")
            screenshots.append(screenshot_path)
            result_the_store[order_id] = ['Error']

        finally:
            time.sleep(5)
            counter_for_done += 1
            logger.info(f'Order done: {counter_for_done}/{number_of_orders}')

    driver.quit()
    return result_the_store, screenshots
