import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from balance_history import *

def plot_transactions(address):
    transactions = fetch_transactions(address)
    plot_data = calculate_balance_history(transactions, address)

    xaxis = []
    yaxis = []

    for timestamp, balance in plot_data:
        date = datetime.fromtimestamp(int(timestamp))
        xaxis.append(date)
        yaxis.append(balance)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(xaxis, yaxis, marker='o')  # 'o' for circle markers

    # Determine the time range in months
    if len(xaxis) > 1:
        time_range = (xaxis[-1] - xaxis[0]).days / 30
        if time_range <= 3:
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        elif 3 < time_range <= 6:
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
            ax.xaxis.set_minor_locator(mdates.DayLocator(interval=5))  # Show every 5th day
            ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
            ax.tick_params(axis='x', which='minor', pad=20)
            #for label in ax.get_xticklabels(which='minor'):
                #label.set_rotation(45)  # Rotate labels to avoid overlap
            for label in ax.get_xticklabels(which='major'):
                label.set_fontsize(10)  # Reduce font size if necessary
                label.set_fontweight('bold')  # Enhance month labels
        else:
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    ax.set_title('Account balance over time')
    #ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.grid(True)

    return fig  # Return the figure object to be used in PyQt6
