import sys
import customtkinter as ctk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph_builder import plot_transactions
from balance_history import process_transaction, fetch_transactions
from utils import get_balance, image_loader

# HEX codes for UI colors
orange = "#F7931A"
light_orange = "#F8D7AE"

# BTC logo path 
btc_logo_url = 'resources/bitcoin-seeklogo.svg'

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set some window properties
        self.title("Sats Manager")
        self.geometry("1800x765")
        self.resizable(False, False)
        self.configure(fg_color = 'white')
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 3)

# =================================== UI ADDRESS ENTRY FRAME =================================================

        # Create frame for entry filed and submit button
        self.entry_frame = ctk.CTkFrame(self,
                                        fg_color = "transparent",
                                        border_width = 1,
                                        border_color = orange,
                                        width = 600,
                                        height = 125)
        
        self.entry_frame.grid(column = 0,
                              row = 0,
                              sticky = "ew",
                              padx = 10,
                              pady = 10)
        
        self.entry_frame.grid_columnconfigure(0, weight = 1)
        self.entry_frame.grid_propagate(False)

        # Initialize and place custom widgets into entry_frame
        self.input_field = ctk.CTkEntry(self.entry_frame, 
                                        placeholder_text = "Enter address", 
                                        fg_color = "#180E1B",
                                        text_color = "white",
                                        font = ("MiriamLibre-Regular", 20), 
                                        justify = "center")
        
        self.input_field.grid(column = 0,
                              row = 0,
                              sticky = "ew",
                              padx = 10,
                              pady = 10)
        
        self.button = ctk.CTkButton(self.entry_frame, 
                                    text = "SEE TRANSACTIONS",
                                    text_color = "white",
                                    font = ("MiriamLibre-Regular", 25),
                                    fg_color = "#F7931A",
                                    command = self.on_button_clicked)
        
        self.button.grid(column = 0,
                         row = 1,
                         padx = 10,
                         pady = 15)
        
        # Change colors on hover
        self.button.bind("<Enter>", lambda event: self.button.configure(fg_color = "white", text_color = "black", border_width = 2, border_color = orange)) 
        self.button.bind("<Leave>", lambda event: self.button.configure(fg_color = orange, text_color = "white"))
        self.bind("<Return>", lambda event: self.on_button_clicked)

# =================================== UI BALANCE FRAME =================================================

        self.balance_frame= ctk.CTkFrame(self,
                                        fg_color = "transparent",
                                        border_width = 1,
                                        border_color = orange,
                                        width = 800,
                                        height = 125)
        
        self.balance_frame.grid(column = 1,
                                row = 0,
                                sticky = "nsew",
                                padx = 10,
                                pady = 10,
                                columnspan = 2)
        
        self.balance_frame.grid_columnconfigure(0, weight = 1)
        self.balance_frame.grid_propagate(False)

        self.balance_label = ctk.CTkLabel(self.balance_frame, text = "", image = image_loader(btc_logo_url, 0.25))
        
        self.balance_label.grid(column = 0,
                                row = 0,
                                sticky = "ns",
                                padx = 10,
                                pady = 20)

# =================================== UI PLOT FRAME =================================================

        self.plot_frame = ctk.CTkFrame(self,
                                        fg_color = "transparent",
                                        border_width = 1,
                                        border_color = orange,
                                        width = 600,
                                        height = 600)
        
        self.plot_frame.grid(column = 0,
                             row = 1,
                             sticky = "new",
                             padx = 10,
                             pady = 10)
        
        self.plot_frame.grid_columnconfigure(0, weight = 1)
        self.plot_frame.grid_propagate(False)
        
        self.plot_label = ctk.CTkLabel(self.plot_frame, text = "", image = image_loader(btc_logo_url, 0.25))

        self.plot_label.grid(column = 0,
                             row = 0,
                             sticky = "nsew",
                             padx = 10,
                             pady = 260)
        
# =================================== UI TRANSACTIONS FRAME =================================================

        self.transactions_frame= ctk.CTkFrame(self,
                                        fg_color = "transparent",
                                        border_width = 1,
                                        border_color = orange,
                                        width = 800,
                                        height = 600)
        
        self.transactions_frame.grid(column = 1,
                                     row = 1,
                                     sticky = "ew",
                                     padx = 10,
                                     pady = 10,
                                     columnspan = 2)
        
        self.transactions_frame.grid_columnconfigure(0, weight = 1)
        self.transactions_frame.grid_propagate(False)
        
        
        self.transactions_label = ctk.CTkLabel(self.transactions_frame, text = "", image = image_loader(btc_logo_url, 0.25))

        self.transactions_label.grid(column = 0,
                                     row = 0,
                                     sticky = "ew",
                                     padx = 10,
                                     pady = 260)

# ===============================================================================================

        self.canvas = None  # Placeholder for the matplotlib canvas

# =================================== UI EVENTS =================================================

    def on_button_clicked(self):
        input_text = self.input_field.get()  # Get text from input field (address)

        global sats, btc 
        sats, btc = get_balance(input_text) # Use get_balance to retrieve address balance and store both the sats and btc amounts
        
        # Update label text to show the balance instead of placeholder image
        if sats is not None:
            self.balance_label.grid_remove()
            self.balance_label = ctk.CTkLabel(self.balance_frame, text = f"Balance: {sats:,} sats",text_color = "black", font = ("MiriamLibre-Regular", 50))
            
            self.balance_label.grid(column = 0,
                                    row = 0,
                                    sticky = "wns",
                                    padx = 10,
                                    pady = 10)
            
            self.balance_label.bind("<Button-1>", self.on_balance_clicked)

            fig, numTransactions = plot_transactions(input_text)

            self.numTransactions_label = ctk.CTkLabel(self.balance_frame, text = f"{len(numTransactions):,} recorded transactions",text_color = "black", font = ("MiriamLibre-Regular", 25))
            
            self.numTransactions_label.grid(column = 0,
                                    row = 1,
                                    sticky = "wns",
                                    padx = 10,
                                    pady = 5)
            
            self.save_button = ctk.CTkButton(self.balance_frame, 
                                    text = "Export Transactions\nCSV",
                                    text_color = "white",
                                    font = ("MiriamLibre-Regular", 15),
                                    fg_color = "#F7931A")
        
            self.save_button.grid(column = 1,
                            row = 0,
                            rowspan = 2,
                            padx = 10,
                            pady = 10)
            
            self.save_button.bind("<Enter>", lambda event: self.save_button.configure(fg_color = "white", text_color = "black", border_width = 2, border_color = orange)) 
            self.save_button.bind("<Leave>", lambda event: self.save_button.configure(fg_color = orange, text_color = "white"))

            if self.canvas is None:
                self.canvas = FigureCanvasTkAgg(fig, self.plot_frame)
                self.canvas.draw()
                self.canvas.get_tk_widget().grid(column = 0,
                                                 row = 0,
                                                 sticky = "wns")
            
            else:
                self.canvas.figure = fig
                self.canvas.draw()
        else:
            self.balance_label.configure(text="Failed to fetch balance", image = "")

        columns = ('TX #', 'Date', 'Type', 'Value', 'Fee')
        tree = ttk.Treeview(self.transactions_frame,
                            columns=columns,
                            show='headings')

        style = ttk.Style()
        style.theme_use("default")  # Ensures compatibility with customtkinter

        # Modify the style of the Treeview
        style.configure("Treeview", background="white", fieldbackground="white", foreground="black")

        # Modify the style of the headings in the Treeview
        style.configure("Treeview.Heading", background="white", foreground="black")

        # Set headings and column configurations
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, width=100, anchor='center')

        # Assuming abc() function handles the API call and returns formatted transactions
        transactions_data = process_transaction(fetch_transactions(input_text), input_text)  # Pass appropriate parameters

        # Iterate over transactions and populate the treeview
        i = 1
        for index, tx in enumerate(transactions_data):
            if tx['value'] != 0:
                tree.insert('', 'end', values=(i, tx['date'], tx['type'], tx['value'], tx['fee']))
            else:
                continue
            i+=1

        # Integrate the Treeview into a ctk.CTkScrollbar for scroll functionality
        scrollbar = ctk.CTkScrollbar(self.transactions_frame, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(column=1, row=0, sticky='ns')
        tree.grid(column=0, row=0, sticky="wens")






    def on_balance_clicked(self, event):
        label_text = self.balance_label.cget('text')

        # Toggle between sats and BTC when label is clicked
        if "sats" in label_text:
            self.balance_label.configure(text=f"Balance: {btc} BTC")
        else:
            self.balance_label.configure(text=f"Balance: {sats:,} sats")


def main():
    window = MainWindow()
    window.mainloop()

if __name__ == "__main__":
    main()
