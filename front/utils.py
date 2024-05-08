from bitcoinlib.wallets import Wallet, wallet_create_or_open
from bitcoinlib.services.services import Service
from PIL import Image, ImageTk
import cairosvg
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

