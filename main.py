from modules.csv_read_and_classify import classify_order_id
from modules.scrapper_thestore import scrap_status_thestore
from modules.scrapper_webstore import track_order_web
from modules.dump_to_csv import dump_to_csv
import pandas as pd

if __name__ == "__main__":
    income_df = pd.read_csv('income/test1.csv')
    thestore_orders_ids, webstore_orders_ids = classify_order_id(income_df)
    print("TheStore Orders IDs:", thestore_orders_ids)
    the_results = scrap_status_thestore(thestore_orders_ids)
    print("TheStore Results:", the_results)
    print("WebStore Orders IDs:", webstore_orders_ids)
    web_results = track_order_web(webstore_orders_ids) or {}
    print("WebStore Results:", web_results)
    all_results = {**the_results, **web_results}
    print("All Results:", all_results)
    
    # Dump results to CSV
    dump_to_csv(all_results, 'output/orders.csv')
