import requests
from datetime import datetime

def fetch_transactions(address):
    # Fetch transaction data for a Bitcoin address from the mempool.space API.
    url = f"https://mempool.space/api/address/{address}/txs"
    response = requests.get(url)
    transactions = []

    while True:
        response = requests.get(url)
        new_transactions = response.json()
        if not new_transactions:
            break
        else:
            transactions.extend(new_transactions)
            last_txid = new_transactions[-1]['txid']
            url = f"https://mempool.space/api/address/{address}/txs/chain/{last_txid}"

        if response.status_code != 200:
            print("Failed to fetch data:", response.status_code)
            break

    return transactions



def calculate_balance_history(transactions, address):
    """Calculate the balance history from transaction data."""
    balance_history = []
    current_balance = 0

    # Assume transactions are listed from newest to oldest, reverse to start from the first
    transactions.reverse()

    for tx in transactions:
        received = 0
        sent = 0

        # Calculate received by looking at outputs (vout)
        for output in tx['vout']:
            if 'scriptpubkey_address' in output and address in output['scriptpubkey_address']:
                received += output['value']

        # Calculate sent by looking at inputs (vin), but only if it's not a coinbase transaction
        if 'is_coinbase' not in tx or not tx['is_coinbase']:
            for input_tx in tx['vin']:
                if 'prevout' in input_tx and 'scriptpubkey_address' in input_tx['prevout'] and address in input_tx['prevout']['scriptpubkey_address']:
                    sent += input_tx['prevout']['value']

        current_balance += (received - sent)
        balance_history.append((tx['status']['block_time'], current_balance))

    return balance_history



def process_transaction(transactions, address):
    """Record and store transaction number, date, type (spend or receive), value, and fee."""
    transaction_details = []

    # Assume transactions are listed from newest to oldest
    for tx in transactions:
        timestamp = tx['status']['block_time']
        date = datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y %H:%M:%S')
        
        # Process each output to determine if it's a received transaction
        for output in tx['vout']:
            if 'scriptpubkey_address' in output and address in output['scriptpubkey_address']:
                transaction = {
                    'date': date,
                    'type': 'receive',
                    'value': output['value'],
                    'fee': tx.get('fee', 0)
                }
                transaction_details.append(transaction)

        # Process inputs if it's not a coinbase transaction to determine sent transactions
        if 'is_coinbase' not in tx or not tx['is_coinbase']:
            total_sent = 0
            total_value_inputs = 0
            for input_tx in tx['vin']:
                if 'prevout' in input_tx and 'scriptpubkey_address' in input_tx['prevout'] and address in input_tx['prevout']['scriptpubkey_address']:
                    total_sent += input_tx['prevout']['value']
                    total_value_inputs += input_tx['prevout']['value']

            transaction = {
                'date': date,
                'type': 'send',
                'value': total_sent,
                'fee': tx.get('fee', 0)
            }
            transaction_details.append(transaction)

    return transaction_details



#'bc1pxav32udnt0062dlvmjn7tp3qneamudpg492t7qmxsu7m73ldd7uq768q8p'

