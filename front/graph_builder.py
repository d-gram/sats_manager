import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from balance_history import *
from matplotlib.ticker import FuncFormatter

def format_ticks(value, pos):
    if value >= 1_000_000:  # Values in millions
        return f'{value / 1_000_000:.1f}M'
    elif value >= 10_000:   # Values in thousands
        return f'{value / 1_000}K'
    else:                   # Values below 10,000
        return str(int(value))

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
    ax.plot(xaxis, yaxis, marker=',', color='#F7931A')

    # Set up date formatting based on time range
    if len(xaxis) > 1:
        time_range = (xaxis[-1] - xaxis[0]).days / 30
        if time_range <= 3:
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        elif 3 < time_range <= 6:
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
            ax.xaxis.set_minor_locator(mdates.DayLocator(interval=10))
            ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
            ax.tick_params(axis='x', which='minor', pad=20, colors='white')
            for label in ax.get_xticklabels(which='major'):
                label.set_fontsize(10)
                label.set_fontweight('bold')
        else:
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    ax.set_title('Account Balance History (Sats)')
    fig.set_facecolor('#180E1B')
    ax.set_facecolor('#180E1B')
    ax.yaxis.set_major_formatter(FuncFormatter(format_ticks))
    ax.grid(True)
    
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    return fig, xaxis  # Return the figure object to be used in PyQt6

