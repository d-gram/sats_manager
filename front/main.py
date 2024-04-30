import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import pyqtSignal
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from graph_builder import plot_transactions
from utils import *

class Button(QPushButton):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.initUI()

    def initUI(self):
        self.clicked.connect(self.on_click)

    def on_click(self):
        return

class Input(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setPlaceholderText("Enter address")

class Label(QLabel):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)  # Initialize the superclass with the provided text and parent
        self.initUI()

    def initUI(self):
        # Custom UI settings for the label
        # self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # You can add more custom properties, such as font, color, etc.
        # Example: Set font size and make it bold
        font = self.font()
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)
        # Set minimum size if you want to ensure a specific look
        # self.setMaximumSize(0,0)
    # If you want to add custom behavior, like reacting to events, you can override event handlers.
    # For example, here's how you'd override the mousePressEvent to print something when clicked.

    clicked = pyqtSignal(object, object)

    def mousePressEvent(self, event):
        self.clicked.emit(sats, btc)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set some window properties
        self.setWindowTitle("Window")
        self.setGeometry(100, 100, 400, 200)

        # Initialize custom widgets
        self.input_field = Input()
        self.button = Button("Submit")
        self.custom_label = Label()
        self.custom_label.setVisible(False)
        self.canvas = None

        # Set up the layout
        self.layout = QVBoxLayout()  # Vertical layout
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.custom_label)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Connecting button click to an action
        self.button.clicked.connect(self.on_button_clicked)
        self.custom_label.clicked.connect(self.on_balance_clicked)

    def on_button_clicked(self):
        # Action to perform when button is clicked
        input_text = self.input_field.text()  # Get text from input field
        #print(f"Button clicked! Input field contains: {input_text}")
        global sats, btc
        sats, btc = get_balance(input_text)
        transactions = get_transactions(input_text)
        
        # Update label text
        if sats != None:
            self.custom_label.setVisible(True)
            self.custom_label.setText(f"Balance: {sats} sats")
            if self.canvas == None:
                fig = plot_transactions(transactions)
                self.canvas = FigureCanvas(fig)
                layout = self.centralWidget().layout()  # Get the current layout from central widget
                layout.addWidget(self.canvas)  # Add the canvas to the layout
            else:
                self.canvas.figure.clear()
                plot_transactions(transactions)
                self.canvas.draw()

            self.canvas.setVisible(True)
        else:
            self.custom_label.setVisible(True)
            self.custom_label.setText("Failed to fetch balance")


    def on_balance_clicked(self, sats, btc):
        label_text = self.custom_label.text()
        # Check the label text and act accordingly
        if "sats" in label_text:
            self.custom_label.setText(f"Balance: {btc} BTC")
        else:
            self.custom_label.setText(f"Balance: {sats} sats")


        

def main():
    app = QApplication(sys.argv)  # Create an application object
    window = MainWindow()         # Create a window object
    window.show()                 # Display the window
    sys.exit(app.exec())          # Start the application's event loop

if __name__ == "__main__":
    main()
