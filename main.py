# main.py
from modules.csv_read_and_classify import classify_order_id
from modules.scrapper_thestore import scrap_status_thestore
import pandas as pd 

# income_df = pd.read_csv('income/test1.csv')
# thestore_orders_ids, webstore_orders_ids = classify_order_id(income_df)


# def create_driver():
#     # Initialize the WebDriver with the configuration details
#     driver = webdriver.Chrome(service=CHROME_SERVICE, options=CHROME_OPTIONS)
#     return driver


if __name__ == "__main__":
    income_df = pd.read_csv('income/test1.csv')
    thestore_orders_ids, webstore_orders_ids = classify_order_id(income_df)
    print(thestore_orders_ids)
    print(scrap_status_thestore(thestore_orders_ids))
    
 