import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from balance_history import *


def plot_transactions(address):
    transactions = fetch_transactions(address)
    plot_data = calculate_balance_history(transactions, address)

    xaxis = []
    yaxis = []

    for timestamp, balance in plot_data:
        xaxis.append(time.strftime('%Y-%m-%d', time.gmtime(int(timestamp))))
        yaxis.append(balance)

    x = list(xaxis)
    y = list(yaxis)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, marker='o')  # 'o' for circle markers

    # Set x-axis tick positions and labels
   # Set x-axis to only display every 5th label
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  # Display a tick every 5 indices




    ax.set_title('Account balance over time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.grid(True)  # Optional, adds a grid to the plot

    return fig  # Return the figure object to be used in PyQt6

