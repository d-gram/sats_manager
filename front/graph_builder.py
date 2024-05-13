import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from balance_history import *
from matplotlib.ticker import FuncFormatter

def format_ticks(value, pos):
    if value >= 100_000_000:  # Values in millions
        return f'{value / 10_000_000:.1f}M'
    elif value >= 10_000:   # Values in thousands
        return f'{value / 10_000}K'
    else:                   # Values below 10,000
        return str(int(value))

def plot_transactions(transactions_dict):
    dates = []
    balance = 0  # Initialize balance to zero
    balance_history = []  # List to store balance history
    current_year = datetime.now().year  # Get the current year

    for tx in transactions_dict:
        # Convert date string to datetime object
        date_obj = datetime.strptime(tx['date'], '%d.%m.%Y %H:%M:%S')
        dates.append(date_obj)
        if tx['type'] == 'spend':
            balance -= tx['value'] + tx['fee']
        elif tx['type'] == 'receive':
            balance += tx['value']
        balance_history.append(balance)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, balance_history, marker=',', color='#F7931A')

    # Set up date formatting based on whether transactions are in the current year
    if len(dates) > 1:
        if any(date.year < current_year for date in dates):
            # Transactions from previous years
            major_locator = mdates.MonthLocator()  # Every month
            major_formatter = mdates.DateFormatter('%b %Y')  # 'Jan 2020'
        else:
            # Transactions from the current year
            major_locator = mdates.MonthLocator()  # Every month
            major_formatter = mdates.DateFormatter('%b %d')  # 'Jan 30'

        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_major_formatter(major_formatter)
    
    ax.set_title('Balance History (Sats)')
    fig.set_facecolor('#180E1B')
    ax.set_facecolor('#180E1B')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.grid(True)
    
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    return fig


