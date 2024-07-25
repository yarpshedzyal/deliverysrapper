import pandas as pd

def dump_to_csv(data, file_path, carrier_dict):
    # Create a list to hold rows of data
    rows = []
    
    # Iterate over the dictionary to extract order details
    for order_number, details in data.items():
        if isinstance(details, list):
            order_status = details[0]
            multi_track = 'No'
            if len(details) > 1 and isinstance(details[1], list):
                if len(details[1]) > 1:
                    multi_track = 'Yes'
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
                        'tracker_number': shipment.get('Tracking Number', 'N/A'),
                        'carrier': carrier,
                        'MultiTrack': multi_track,
                        'proper_carrier': proper_carrier
                    }
                    rows.append(row)
            else:
                row = {
                    'order_number': order_number,
                    'order_status': order_status,
                    'tracker_number': 'N/A',
                    'carrier': 'N/A',
                    'MultiTrack': multi_track,
                    'proper_carrier': 'No'
                }
                rows.append(row)
        else:
            order_status, tracker_number = details
            proper_carrier = 'No'
            row = {
                'order_number': order_number,
                'order_status': order_status,
                'tracker_number': tracker_number,
                'carrier': 'N/A',
                'MultiTrack': 'No',
                'proper_carrier': proper_carrier
            }
            rows.append(row)

    # Create a DataFrame from the rows
    df = pd.DataFrame(rows, columns=['order_number', 'order_status', 'tracker_number', 'carrier', 'MultiTrack', 'proper_carrier'])
    
    # Write the DataFrame to a CSV file
    df.to_csv(file_path, index=False)

    print(f"Data successfully written to {file_path}")
