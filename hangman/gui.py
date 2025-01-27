import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,QComboBox,QMessageBox,QHBoxLayout,QLineEdit
from PyQt6.QtCore import Qt
import random

def load_word(category):
    file_map = {
        "Fruits": "fruits.txt",
        "Spices": "spices.txt",
        "Veggies": "veggies.txt",
        "Other": "other.txt",
    }
    file_path = file_map.get(category, None)
    if not file_path:
        return None

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            return random.choice(lines).strip().lower()
    except FileNotFoundError:
        return None
class HangmanGame(QMainWindow):
    def __init__(self, category):
        super().__init__()
        self.setWindowTitle(f"Hangman - {category}")
        self.setGeometry(100, 100, 500, 300)

        self.word = load_word(category)
        if not self.word:
            QMessageBox.critical(self, "Error", f"Could not load words for category '{category}'.")
            self.close()
            return

        self.guessed_letters = ""
        self.remaining_chances = len(self.word) + 2

        # Main layout
        layout = QVBoxLayout()

        # Display the word
        self.word_display = QLabel("_ " * len(self.word))
        self.word_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.word_display)

        # Input and guess button
        input_layout = QHBoxLayout()
        self.guess_input = QLineEdit()
        self.guess_input.setPlaceholderText("Enter a letter")
        self.guess_input.returnPressed.connect(self.make_guess)
        self.guess_button = QPushButton("Guess")
        self.guess_button.clicked.connect(self.make_guess)
        input_layout.addWidget(self.guess_input)
        input_layout.addWidget(self.guess_button)
        layout.addLayout(input_layout)

        # Status display
        self.status_label = QLabel(f"Chances left: {self.remaining_chances}")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Set layout to central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.update_display()

    def update_display(self):
        display = ""
        for char in self.word:
            if char in self.guessed_letters:
                display += char + " "
            elif char == " ":
                display += "  "
            else:
                display += "_ "
        self.word_display.setText(display.strip())

    def make_guess(self):
        guess = self.guess_input.text().lower()
        self.guess_input.clear()

        if len(guess) != 1 or not guess.isalpha():
            QMessageBox.warning(self, "Invalid Input", "Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            QMessageBox.information(self, "Already Guessed", f"You already guessed '{guess}'.")
            return

        self.guessed_letters += guess

        if guess in self.word:
            self.update_display()
            if "_" not in self.word_display.text():
                QMessageBox.information(self, "Congratulations", "You guessed the word!")
                self.close()
        else:
            self.remaining_chances -= 1
            self.status_label.setText(f"Chances left: {self.remaining_chances}")
            if self.remaining_chances <= 0:
                QMessageBox.critical(self, "Game Over", f"You've run out of chances! The word was '{self.word}'.")
                self.close()
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Hangman")
        self.setGeometry(100, 100, 400, 300)  # x, y, width, height
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Add a layout
        layout = QVBoxLayout()
        
        # Add a label
        self.label = QLabel("Select a category", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.dropdown = QComboBox()
        self.dropdown.addItems((["Fruits", "Spices", "Veggies", "Other"]))
        layout.addWidget(self.dropdown)
        
       # Button to start the game
        self.start_button = QPushButton("Start Game")
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button)

        # Set layout
        central_widget.setLayout(layout)

    def start_game(self):
        selected_category = self.dropdown.currentText()
        self.game_window = HangmanGame(selected_category)
        self.game_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())