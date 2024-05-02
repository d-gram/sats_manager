from bitcoinlib.wallets import Wallet, wallet_create_or_open
from bitcoinlib.services.services import Service
import requests
import time

def get_balance(address):
    try:
        # Create or open a temporary wallet (not used for transactions, only for balance checking)
        w = wallet_create_or_open('temp_wallet', network='bitcoin', witness_type='legacy', keys=address)

        # Use the default service provider, or you can specify another provider
        service = Service()
        balance = service.getbalance(address)

        # Close and delete the wallet as it is not needed anymore
        # w.delete()

        return balance, format_number(balance, 8)
    except Exception as e:
        print(f"Error fetching balance: {str(e)}")
        return None
    
def format_number(number, padding):
    # Calculate the integer and fractional parts
    integer_part = int(number // 100000000)
    fractional_part = int(number % 100000000)

    # Format the number to ensure the fractional part has 8 digits (leading zeroes if necessary)
    formatted_number = f"{int(integer_part)}.{fractional_part:0{padding}d}"
    
    return formatted_number
'''
def get_transactions(address):
    url = f"https://blockchain.info/rawaddr/{address}"
    response = requests.get(url)
    if response.status_code == 200:
        transactions = response.json()["txs"]
        transaction_details = []  # List to store details for all transactions
        for transaction in transactions:
            raw_time = int(transaction["time"])
            date = time.strftime('%Y-%m-%d', time.gmtime(raw_time))
            balance = format_number(transaction["balance"], 8)
            transaction_details.append((date, balance))
        return transaction_details
    else:
        print("Error retrieving transactions")
        return []'''
