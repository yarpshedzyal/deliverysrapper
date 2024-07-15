import pandas as pd

def dump_to_csv(data, file_path):
    # List of proper carriers
    proper_carriers = [
        "4PX", "A-1", "AAA Cooper", "ABF", "Asendia", "Best Buy", "Blue Package", "Canada Post", "CEVA", "China Post", 
        "Conway", "DHL", "DHL eCommerce", "Estes", "FedEx", "Fedex Freight", "FedEx SmartPost", "First Mile", 
        "Hongkong Post", "Hunter Logistics", "India Post", "JCEX", "Lasership", "Newgistics", "Old Dominion", 
        "OnTrac", "OSM", "Pilot Freight", "R+L", "Roadrunner", "Royal Mail", "Saia", "SF Express", "SFC", 
        "South Eastern Freight Lines", "StreamLite", "UPS", "UPS Freight", "UPS Mail Innovations", "Urban Express", 
        "USPS", "Watkins and Shepard", "XPO Freight", "Yanwen", "Yellow Freight", "Yun Express", "CyberSavings", 
        "YF Logistics", "YHT", "Landmark", "ShipEntegra", "Cainiao", "Letian", "PTT Kargo"
    ]
    
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
                    proper_carrier = 'Yes' if carrier in proper_carriers else 'No'
                    row = {
                        'order_number': order_number,
                        'order_status': order_status,
                        'tracker_number': shipment.get('Tracking Number', 'N/A'),
                        'carrier': carrier,
                        'MultiTrack': multi_track,
                        'proper_carrier': proper_carrier  # Add proper_carrier to the row
                    }
                    rows.append(row)
            else:
                row = {
                    'order_number': order_number,
                    'order_status': order_status,
                    'tracker_number': 'N/A',
                    'carrier': 'N/A',
                    'MultiTrack': multi_track,
                    'proper_carrier': 'No'  # Add proper_carrier to the row
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
                'proper_carrier': proper_carrier  # Add proper_carrier to the row
            }
            rows.append(row)

    # Create a DataFrame from the rows
    df = pd.DataFrame(rows, columns=['order_number', 'order_status', 'tracker_number', 'carrier', 'MultiTrack', 'proper_carrier'])
    
    # Write the DataFrame to a CSV file
    df.to_csv(file_path, index=False)

    print(f"Data successfully written to {file_path}")
