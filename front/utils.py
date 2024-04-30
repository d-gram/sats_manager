from bitcoinlib.wallets import Wallet, wallet_create_or_open
from bitcoinlib.services.services import Service

def get_balance(address):
    try:
        # Create or open a temporary wallet (not used for transactions, only for balance checking)
        w = wallet_create_or_open('temp_wallet', network='bitcoin', witness_type='legacy', keys=address)

        # Use the default service provider, or you can specify another provider
        service = Service()
        balance = service.getbalance(address)

        # Close and delete the wallet as it is not needed anymore
        # w.delete()

        return balance
    except Exception as e:
        print(f"Error fetching balance: {str(e)}")
        return None
    

