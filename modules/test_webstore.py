from bs4 import BeautifulSoup
import requests

def create_tracking_url(order_number, email):
    base_url = "https://www.webstaurantstore.com/myaccount:trackorder/ordertracking/order_number/*/email/*/"
    tracking_url = base_url.replace("order_number/*", f"order_number/{order_number}").replace("email/*", f"email/{email}")
    return tracking_url

def check_status_webstore(order_number, email):
    url = create_tracking_url(order_number, email)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Here you can add code to scrape specific data from the page
        return soup
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

mail = 'kaatzeboo@gmail.com'
order_num = '99237672'   

order_page = check_status_webstore(order_num, mail)

if order_page:
    # Process the BeautifulSoup object 'order_page' as needed
    print(order_page.prettify())
