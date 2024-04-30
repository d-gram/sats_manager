import matplotlib.pyplot as plt

def plot_transactions(transactions):
    if transactions:
        dates = [item[0] for item in transactions[::-1]]
        values = [item[1] for item in transactions] 

        plt.figure(figsize=(10, 5))  # You can adjust the figure size to your needs
        plt.plot(dates, sorted(values), marker='o')  # 'o' for circle markers

        # Improve the x-axis date labels readability
        plt.gcf().autofmt_xdate()  # Auto formats the x-axis labels to fit them in the plot

        plt.title('Account balance over time')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.grid(True)  # Optional, adds a grid to the plot
        plt.show()
    else:
        print("No transactions found for the given address")
