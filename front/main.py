import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QLabel
from utils import get_balance

class CustomButton(QPushButton):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.initUI()

    def initUI(self):
        self.clicked.connect(self.on_click)

    def on_click(self):
        print("Button Clicked!")

class CustomInput(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setPlaceholderText("Enter address")

class CustomLabel(QLabel):
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
        self.setMaximumSize(0,0)
    '''
    # If you want to add custom behavior, like reacting to events, you can override event handlers.
    # For example, here's how you'd override the mousePressEvent to print something when clicked.
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print('Label clicked!')
        # Don't forget to call the superclass method to ensure the event system works correctly.
        super().mousePressEvent(event)
    '''



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set some window properties
        self.setWindowTitle("Window")
        self.setGeometry(100, 100, 400, 200)

        # Initialize custom widgets
        self.input_field = CustomInput()
        self.button = CustomButton("Submit")
        self.custom_label = CustomLabel()

        # Set up the layout
        layout = QVBoxLayout()  # Vertical layout
        layout.addWidget(self.input_field)
        layout.addWidget(self.button)
        layout.addWidget(self.custom_label)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connecting button click to an action
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        # Action to perform when button is clicked
        input_text = self.input_field.text()  # Get text from input field
        print(f"Button clicked! Input field contains: {input_text}")
        balance = get_balance(input_text)
        
        # Update label text
        if balance != None:
            self.setMaximumSize(200, 50)
            self.custom_label.setText(f"Balance: {balance} satoshis")
            print(f"Balance of {input_text} is {balance}")
        else:
            self.setMaximumSize(200, 50)
            self.custom_label.setText("Failed to fetch balance")
            print("fetch error")

        

def main():
    app = QApplication(sys.argv)  # Create an application object
    window = MainWindow()         # Create a window object
    window.show()                 # Display the window
    sys.exit(app.exec())          # Start the application's event loop

if __name__ == "__main__":
    main()
