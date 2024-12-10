import sys
import random
import string
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QSpinBox, QCheckBox, QPushButton, 
    QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QProgressBar, QFileDialog
)
from PyQt5.QtGui import QFont, QGuiApplication, QColor
from PyQt5.QtCore import Qt


class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the User Interface."""
        # Window setup
        self.setWindowTitle("Advanced Password Generator")
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet("background-color: #f2f2f2;")

        # Title
        title_label = QLabel("🔒 Password Generator 🔒")
        title_label.setFont(QFont("Arial", 22, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")

        # Password Length Input
        length_label = QLabel("Password Length:")
        self.length_spinbox = self.create_spinbox(4, 64, 12)

        # Options for character inclusion
        self.include_uppercase = self.create_checkbox("Include Uppercase Letters", True)
        self.include_numbers = self.create_checkbox("Include Numbers", True)
        self.include_symbols = self.create_checkbox("Include Symbols", True)

        # Exclude specific characters
        exclude_label = QLabel("Exclude Characters:")
        self.exclude_characters = self.create_line_edit("Enter characters to exclude...")

        # Buttons
        generate_button = self.create_button("Generate Password", "#3498db", self.generate_password)
        save_button = self.create_button("Save Password to File", "#27ae60", self.save_password)
        copy_button = self.create_button("Copy to Clipboard", "#e67e22", self.copy_to_clipboard)

        # Password output
        self.password_output = QLineEdit()
        self.password_output.setReadOnly(True)
        self.password_output.setStyleSheet(
            "padding: 10px; font-size: 16px; background-color: #ecf0f1; border: 1px solid #bdc3c7;"
        )

        # Password strength display
        self.strength_label = QLabel("Password Strength: Not Evaluated")
        self.strength_label.setStyleSheet("font-size: 14px; color: #7f8c8d; margin-top: 10px;")

        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setStyleSheet(
            "QProgressBar { text-align: center; } QProgressBar::chunk { background-color: #3498db; }"
        )

        # Layouts
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addLayout(self.create_horizontal_layout(length_label, self.length_spinbox))
        main_layout.addWidget(self.include_uppercase)
        main_layout.addWidget(self.include_numbers)
        main_layout.addWidget(self.include_symbols)
        main_layout.addWidget(exclude_label)
        main_layout.addWidget(self.exclude_characters)
        main_layout.addWidget(generate_button)
        main_layout.addWidget(self.password_output)
        main_layout.addWidget(self.strength_label)
        main_layout.addWidget(self.strength_bar)
        main_layout.addWidget(save_button)
        main_layout.addWidget(copy_button)

        self.setLayout(main_layout)

    # Helper Methods for UI Components
    def create_spinbox(self, min_value, max_value, default_value):
        """Create a spinbox for selecting numeric values."""
        spinbox = QSpinBox()
        spinbox.setRange(min_value, max_value)
        spinbox.setValue(default_value)
        spinbox.setStyleSheet("padding: 5px; font-size: 14px;")
        return spinbox

    def create_checkbox(self, text, checked=False):
        """Create a styled checkbox."""
        checkbox = QCheckBox(text)
        checkbox.setChecked(checked)
        checkbox.setStyleSheet("font-size: 14px;")
        return checkbox

    def create_line_edit(self, placeholder=""):
        """Create a styled QLineEdit with a placeholder."""
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet("padding: 5px; font-size: 14px;")
        return line_edit

    def create_button(self, text, color, callback):
        """Create a styled QPushButton."""
        button = QPushButton(text)
        button.setStyleSheet(self.button_style(color))
        button.clicked.connect(callback)
        return button

    def create_horizontal_layout(self, *widgets):
        """Create a horizontal layout for aligning widgets."""
        layout = QHBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        return layout

    # Style Helpers
    def button_style(self, color):
        """Generate a button style with hover effect."""
        def darken_color(color_hex, factor=0.8):
            color = QColor(color_hex)
            r, g, b, _ = color.getRgb()
            r, g, b = max(0, int(r * factor)), max(0, int(g * factor)), max(0, int(b * factor))
            return QColor(r, g, b).name()
        
        hover_color = darken_color(color)
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            font-size: 14px;
            padding: 10px;
            border-radius: 5px;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        """

    # Core Functionality
    def generate_password(self):
        """Generate a random password based on user preferences."""
        length = self.length_spinbox.value()
        exclude = set(self.exclude_characters.text())

        # Build character set
        char_set = set(string.ascii_lowercase)
        if self.include_uppercase.isChecked():
            char_set.update(string.ascii_uppercase)
        if self.include_numbers.isChecked():
            char_set.update(string.digits)
        if self.include_symbols.isChecked():
            char_set.update(string.punctuation)
        
        # Exclude unwanted characters
        char_set.difference_update(exclude)

        if not char_set:
            QMessageBox.warning(self, "Error", "Character set is empty. Adjust options.")
            return

        # Generate password
        password = ''.join(random.SystemRandom().choice(list(char_set)) for _ in range(length))
        self.password_output.setText(password)
        self.evaluate_strength(password)

    def evaluate_strength(self, password):
        """Evaluate password strength based on length and variety."""
        length_score = min(len(password) * 5, 40)
        variety_score = len(set(password)) * 2

        total_score = length_score + variety_score
        if total_score > 80:
            self.strength_label.setText("Password Strength: Strong")
            self.strength_label.setStyleSheet("color: #27ae60; font-size: 14px;")
            self.strength_bar.setValue(100)
        elif total_score > 50:
            self.strength_label.setText("Password Strength: Moderate")
            self.strength_label.setStyleSheet("color: #f39c12; font-size: 14px;")
            self.strength_bar.setValue(75)
        else:
            self.strength_label.setText("Password Strength: Weak")
            self.strength_label.setStyleSheet("color: #e74c3c; font-size: 14px;")
            self.strength_bar.setValue(50)

    def save_password(self):
        """Save the generated password to a file."""
        password = self.password_output.text()
        if password:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Password", "", "Text Files (*.txt);;All Files (*)")
            if file_path:
                with open(file_path, "w") as file:
                    file.write(password)
                QMessageBox.information(self, "Success", "Password saved to file.")
        else:
            QMessageBox.warning(self, "Error", "No password to save.")

    def copy_to_clipboard(self):
        """Copy the password to the system clipboard."""
        password = self.password_output.text()
        if password:
            QGuiApplication.clipboard().setText(password)
            QMessageBox.information(self, "Success", "Password copied to clipboard.")
        else:
            QMessageBox.warning(self, "Error", "No password to copy.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    generator = PasswordGenerator()
    generator.show()
    sys.exit(app.exec_())
