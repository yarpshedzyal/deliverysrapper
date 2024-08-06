import pandas as pd
from functools import wraps

def na_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        rows = func(*args, **kwargs)
        for row in rows:
            if row['tracking_number'] == 'N/A' or row['carrier'] == 'N/A':
                row['order_status'] = 'N/A'
                row['MultiTrack'] = 'N/A'
                row['proper_carrier'] = 'N/A'
                row['mono_carrier_multitrack'] = 'N/A'
        return rows
    return wrapper

@na_decorator
def prepare_rows(data, carrier_dict):
    # Create a list to hold rows of data
    rows = []
    
    # Iterate over the dictionary to extract order details
    for order_number, details in data.items():
        if isinstance(details, list):
            order_status = details[0]
            multi_track = 'No'
            mono_carrier_multitrack = 'No'
            if len(details) > 1 and isinstance(details[1], list):
                if len(details[1]) > 1:
                    multi_track = 'Yes'
                    carriers = [shipment.get('Carrier', 'N/A') for shipment in details[1]]
                    unique_carriers = set(carriers)
                    if len(unique_carriers) == 1:
                        mono_carrier_multitrack = 'Yes'
                for shipment in details[1]:
                    carrier = shipment.get('Carrier', 'N/A')
                    if carrier in carrier_dict:
                        proper_carrier = 'Yes'
                        carrier = carrier_dict[carrier]
                    else:
                        proper_carrier = 'No'
                    row = {
                        'order_number': order_number,
                        'order_status': order_status,
                        'tracking_number': shipment.get('Tracking Number', 'N/A'),
                        'carrier': carrier,
                        'MultiTrack': multi_track,
                        'proper_carrier': proper_carrier,
                        'mono_carrier_multitrack': mono_carrier_multitrack
                    }
                    rows.append(row)
            else:
                row = {
                    'order_number': order_number,
                    'order_status': order_status,
                    'tracking_number': 'N/A',
                    'carrier': 'N/A',
                    'MultiTrack': multi_track,
                    'proper_carrier': 'No',
                    'mono_carrier_multitrack': mono_carrier_multitrack
                }
                rows.append(row)
        else:
            order_status, tracker_number = details
            proper_carrier = 'No'
            row = {
                'order_number': order_number,
                'order_status': order_status,
                'tracking_number': tracker_number,
                'carrier': 'N/A',
                'MultiTrack': 'No',
                'proper_carrier': proper_carrier,
                'mono_carrier_multitrack': 'No'
            }
            rows.append(row)
    return rows

def dump_to_csv(data, file_path, carrier_dict):
    # Get the prepared rows
    rows = prepare_rows(data, carrier_dict)
    
    # Create a DataFrame from the rows
    df = pd.DataFrame(rows, columns=['order_number', 'order_status', 'tracking_number', 'carrier', 'MultiTrack', 'proper_carrier', 'mono_carrier_multitrack'])
    
    # Write the DataFrame to a CSV file
    df.to_csv(file_path, index=False)

    print(f"Data successfully written to {file_path}")
