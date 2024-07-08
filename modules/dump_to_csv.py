import pandas as pd

def dump_to_csv(data, file_path):
    # Create a list to hold rows of data
    rows = []
    
    # Iterate over the dictionary to extract order details
    for order_number, details in data.items():
        if isinstance(details, list):
            order_status = details[0]
            if len(details) > 1 and isinstance(details[1], list):
                for shipment in details[1]:
                    row = {
                        'order_number': order_number,
                        'order_status': order_status,
                        'tracker_number': shipment.get('Tracking Number', 'N/A'),
                        'carrier': shipment.get('Carrier', 'N/A')  # Add carrier to the row
                    }
                    rows.append(row)
            else:
                row = {
                    'order_number': order_number,
                    'order_status': order_status,
                    'tracker_number': 'N/A',
                    'carrier': 'N/A'  # Add carrier to the row
                }
                rows.append(row)
        else:
            order_status, tracker_number = details
            row = {
                'order_number': order_number,
                'order_status': order_status,
                'tracker_number': tracker_number,
                'carrier': 'N/A'  # Add carrier to the row
            }
            rows.append(row)

    # Create a DataFrame from the rows
    df = pd.DataFrame(rows, columns=['order_number', 'order_status', 'tracker_number', 'carrier'])
    
    # Write the DataFrame to a CSV file
    df.to_csv(file_path, index=False)

    print(f"Data successfully written to {file_path}")


