from bitcoinlib.wallets import Wallet, wallet_create_or_open
from bitcoinlib.services.services import Service
from bip_utils import Bip44, Bip44Coins, Bip44Changes, Bip49,  Bip49Coins, Bip84, Bip84Coins
from PIL import Image, ImageTk
from concurrent.futures import ThreadPoolExecutor, as_completed
import cairosvg
import requests
import io

def get_balance(address):
    try:
        # Create or open a temporary wallet (not used for transactions, only for balance checking)
        w = wallet_create_or_open('temp_wallet', network='bitcoin', witness_type='legacy', keys=address)

        # Use the default service provider, or you can specify another provider
        service = Service()
        balance = service.getbalance(address)

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

def image_loader(image_address, opacity):
    png = cairosvg.svg2png(url = image_address, output_width = 80, output_height = 80)
    image = Image.open(io.BytesIO(png))
    alpha = image.getchannel('A')
    alpha = alpha.point(lambda p: p * opacity)  # Adjust opacity to 50%
    image.putalpha(alpha)
    btc_logo = ImageTk.PhotoImage(image)
    return btc_logo


def generate_from_ypub(ypub, num_addresses=20):
    # Assuming that the coin type for Bitcoin should be specified, and the library uses a generalized change parameter
    bip_obj = Bip49.FromExtendedKey(ypub, Bip49Coins.BITCOIN)
    # If the library uses a universal change parameter across BIPs, use it; otherwise adjust accordingly
    ypub_addresses = [
        bip_obj.Change(Bip44Changes.CHAIN_EXT).AddressIndex(i).PublicKey().ToAddress()
        for i in range(num_addresses)
    ]
    return ypub_addresses

def generate_from_zpub(zpub, num_addresses=20):
    # Same as above, specify the coin type
    bip_obj = Bip84.FromExtendedKey(zpub, Bip84Coins.BITCOIN)
    # Use the universal change parameter if that's what the library supports
    zpub_addresses = [
        bip_obj.Change(Bip44Changes.CHAIN_EXT).AddressIndex(i).PublicKey().ToAddress()
        for i in range(num_addresses)
    ]
    return zpub_addresses

def generate_from_xpub(xpub, num_addresses = 20):
    # Create a Bip44 object from the extended public key
    bip_obj = Bip44.FromExtendedKey(xpub, Bip44Coins.BITCOIN)
    # Generate addresses by iterating through the address indices directly from the current level
    xpub_addresses = [
        bip_obj.Change(Bip44Changes.CHAIN_EXT).AddressIndex(i).PublicKey().ToAddress()
        for i in range(num_addresses)
    ]
    return xpub_addresses

def fetch_address_transactions(address):
    print('Fetching transactions using mempool.space API\n')
    url = f"https://mempool.space/api/address/{address}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            tx_count = data['chain_stats']['tx_count']
            if tx_count > 0:
                print(f"Transactions found for {address}: {tx_count}")
                return {'address': address, 'tx_count': tx_count}
            else:
                print(f"No transactions for {address}")
    except requests.RequestException as e:
        print(f"Error fetching data for {address}: {str(e)}")
    return None


def check_addresses(addresses):
    print('Started checking addresses\n')
    non_empty_addresses = []
    for address in addresses:
        result = fetch_address_transactions(address)
        if result:
            non_empty_addresses.append(result['address'])
    return non_empty_addresses

def fetch_detailed_transactions(addresses):
    detailed_transactions = {}
    for address in addresses:
        url = f"https://mempool.space/api/address/{address}/txs"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                transactions = response.json()
                detailed_transactions[address] = transactions
                print(f"Details for {address}: Retrieved {len(transactions)} transactions")
        except requests.RequestException as e:
            print(f"Error fetching detailed transactions for {address}: {str(e)}")
    return detailed_transactions

def generate_and_check(user_input):
    print('inside generate\n')
    # Determine the type of public key based on the prefix in the input string
    if 'xpub' in user_input:
        print('xpub detected\n')
        generated = generate_from_xpub(user_input)
    elif 'ypub' in user_input:
        generated = generate_from_ypub(user_input)
    elif 'zpub' in user_input:
        generated = generate_from_zpub(user_input)
    else:
        raise ValueError("Invalid input! The input must contain xpub, ypub, or zpub.")

    print(f"Addresses Generated: {generated}\n")
    
    print('Checking for non-empty addresses...\n')
    non_empty_addresses = check_addresses(generated)
    print(f"Non-empty addresses: {non_empty_addresses}\n")
    
    if non_empty_addresses:
        print('Fetching detailed transactions...\n')
        return fetch_detailed_transactions(non_empty_addresses)
    else:
        print('No transactions found across all addresses.\n')
        return {}

'''user_input = 'zpub6rn5uko6oSpku6CAB6CUS1zzq9JJJPidZPxKwjH4cRb4mMG2HxqK2PwJLbCstr87J52kqBb98z3u9JiXYxzriHDqJVsouoyMWDYHvDmawgu'
result = generate_and_check(user_input)
print(result)'''

