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

def get_transactions(address):
    url = f"https://blockstream.info/api/address/{address}/txs"
    response = requests.get(url)
    if response.status_code == 200:
        transactions = response.json()["txs"]
        history = []  # List to store details for all transactions
        start_balance = 0
        for tx in transactions:
            txid = tx['txid']
            timestamp = tx['status']['block_time']
            date = time.strftime('%Y-%m-%d', time.gmtime(timestamp))

            # Calculate the balance impact of the transaction
            received = sum(output['value'] for output in tx['vout'] if address in [x['addresses'][0] for x in output['scriptpubkey_address'] if 'addresses' in x])
            sent = sum(input['prevout']['value'] for input in tx['vin'] if address == input['prevout']['scriptpubkey_address'])
            balance_change = received - sent

            # Update current balance based on the transaction
            start_balance += balance_change

            # Append the date and balance change as a tuple
            history.append((date, start_balance))
        for x in history:
            print(x)
        return history
    else:
        print("Error retrieving transactions")
        return []
