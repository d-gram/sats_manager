import csv
import os

# Function to get the desktop path for different OS
def get_desktop_path():
    # Get the home directory
    home = os.path.expanduser('~')
    # Append the desktop path based on common desktop locations
    if os.name == 'nt':  # Windows
        return os.path.join(home, 'Desktop')
    elif os.name == 'posix':  # MacOS or Linux
        return os.path.join(home, 'Desktop')

def save_csv(transaction_details):
    csv_file_path = os.path.join(get_desktop_path(), 'transactions.csv')

    #Writing data to the CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(['TXID', 'Date', 'Type', 'Value', 'Fee'])
        # Write data rows
        for transaction in transaction_details:
            if all(key in transaction for key in ['txid', 'date', 'type', 'value', 'fee']):
                writer.writerow([
                    transaction['txid'],
                    transaction['date'],
                    transaction['type'],
                    str(transaction['value']),  # Convert value to string
                    str(transaction['fee'])     # Convert fee to string
                ])
            else:
                print(f"Missing data in transaction: {transaction}")

    print(f'CSV file has been saved to {csv_file_path}')
    return True
