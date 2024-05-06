import sys
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph_builder import plot_transactions
from utils import get_balance

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set some window properties
        self.title("Window")
        self.geometry("400x200")

        # Initialize custom widgets
        self.input_field = ctk.CTkEntry(self, placeholder_text="Enter address")
        self.button = ctk.CTkButton(self, text="Submit", command=self.on_button_clicked)
        self.custom_label = ctk.CTkLabel(self, text="")
        self.custom_label.pack_forget()  # Hide the label initially
        
        # Customize the font of the label
        self.custom_label.configure(font=("Roboto Medium", 16, "bold"))
        
        # Layout configuration
        self.input_field.pack(pady=10, padx=10, fill="x")
        self.button.pack(pady=10, padx=10, fill="x")
        self.custom_label.pack(pady=10, padx=10, fill="x")

        self.custom_label.bind("<Button-1>", self.on_balance_clicked)

        self.canvas = None  # Placeholder for the matplotlib canvas

    def on_button_clicked(self):
        input_text = self.input_field.get()  # Get text from input field
        global sats, btc
        sats, btc = get_balance(input_text)
        
        # Update label text and show/hide label based on data
        if sats is not None:
            self.custom_label.configure(text=f"Balance: {sats} sats")
            self.custom_label.pack(pady=10, padx=10, fill="x")  # Ensure label is visible
            fig = plot_transactions(input_text)
            if self.canvas is None:
                self.canvas = FigureCanvasTkAgg(fig, self)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(pady=10, padx=10, fill="both", expand=True)
            else:
                self.canvas.figure = fig
                self.canvas.draw()
        else:
            self.custom_label.configure(text="Failed to fetch balance")
            self.custom_label.pack(pady=10, padx=10, fill="x")  # Ensure label is visible

    def on_balance_clicked(self, event):
        label_text = self.custom_label.cget('text')
        # Toggle between sats and BTC when label is clicked
        if "sats" in label_text:
            self.custom_label.configure(text=f"Balance: {btc} BTC")
        else:
            self.custom_label.configure(text=f"Balance: {sats} sats")


def main():
    window = MainWindow()
    window.mainloop()

if __name__ == "__main__":
    main()
