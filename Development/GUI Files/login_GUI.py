from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout, QFormLayout, QDialog


class loginScreen(QFrame):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setGeometry(100, 100, 1600, 1200)
        heading_font = QFont('Times New Roman', 35)
        subheading_font = QFont('Times New Roman', 20)
        welcome = QLabel('Welcome CAST-A-WAY Member')
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setFont(heading_font)
        space = QLabel('  ')
        space.setMinimumWidth(250)
        self.popup = credScreen()

        # Username and Password labels and entries
        username_label = QLabel('Username:')
        username_label.setFont(subheading_font)
        self.username_entry = QLineEdit()
        self.username_entry.setFont(subheading_font)
        self.username_entry.setMaximumWidth(800)
        entry_layout = QFormLayout()
        entry_layout.addRow(username_label, self.username_entry)

        password_label = QLabel('Password:')
        password_label.setFont(subheading_font)
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setFont(subheading_font)
        self.password_entry.setMaximumWidth(800)
        entry_layout.addRow(password_label, self.password_entry)

        # Login button
        self.login_button = QPushButton('Login')
        self.login_button.setFont(subheading_font)
        self.login_button.setMaximumWidth(400)
        self.login_button.clicked.connect(self.login)

        # Forgot Password button
        self.forgot_password_button = QPushButton('Forgot Password?')
        self.forgot_password_button.setFont(subheading_font)
        self.forgot_password_button.setMaximumWidth(650)
        self.forgot_password_button.clicked.connect(self.forgot_password)

        # Error Message
        self.error_message = QLabel("")
        self.error_message.setStyleSheet("color: red;")
        self.error_message.setAlignment(Qt.AlignCenter)

        # Account Creation
        account_button = QPushButton('Create a New Account')
        account_button.clicked.connect(self.show_popup)

        # Layout
        entry = QHBoxLayout()
        entry.addWidget(space)
        entry.addLayout(entry_layout)
        buttons = QVBoxLayout()
        buttons.addWidget(self.login_button)
        buttons.addWidget(self.forgot_password_button)
        buttons.setAlignment(Qt.AlignHCenter)
        layout = QVBoxLayout()
        layout.addWidget(welcome)
        layout.addLayout(entry)
        layout.addLayout(buttons)
        layout.addWidget(self.error_message)
        layout.addWidget(account_button)
        self.setLayout(layout)

    def login(self):
        check = self.check_login()
        if check:
            self.error_message.setText('')
            self.window.home_click()
        else:
            self.error_message.setText('incorrect username or password')

    def forgot_password(self):
        self.forgot_password_button.setText("Password Forgotten")

    def check_login(self):
        # Get user input for the credentials to search
        search_username = self.username_entry.text()
        search_password = self.password_entry.text()

        with open('credentials.txt', 'r') as file:
            # Iterate through each line in the file
            for line in file:
                # Check if the current line exactly matches the search credentials
                if line.strip() == f'Username: {search_username} Password: {search_password}':
                    return True
        return False

    def show_popup(self):
        result = self.popup.exec_()
        if result == QDialog.Accepted:
            print("Popup accepted")
        else:
            print("Popup rejected")

    def close_popup(self):
        self.popup.close()

    def reset(self):
        self.forgot_password_button.setText("Forgot Password")
        self.username_entry.setText('')
        self.password_entry.setText('')


class credScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        subheading_font = QFont('Times New Roman', 15)
        space = QLabel('  ')
        space.setMinimumWidth(250)

        # Username and Password labels and entries
        master_label = QLabel('Master Password:')
        master_label.setFont(subheading_font)
        self.master_entry = QLineEdit()
        self.master_entry.setEchoMode(QLineEdit.Password)
        self.master_entry.setFont(subheading_font)
        self.master_entry.setMaximumWidth(800)
        entry_layout = QFormLayout()
        entry_layout.addRow(master_label, self.master_entry)

        username_label = QLabel('New Username:')
        username_label.setFont(subheading_font)
        self.username_entry = QLineEdit()
        self.username_entry.setFont(subheading_font)
        self.username_entry.setMaximumWidth(800)
        entry_layout.addRow(username_label, self.username_entry)

        password_label = QLabel('New Password:')
        password_label.setFont(subheading_font)
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setFont(subheading_font)
        self.password_entry.setMaximumWidth(800)
        entry_layout.addRow(password_label, self.password_entry)

        password2_label = QLabel('Confirm Password:')
        password2_label.setFont(subheading_font)
        self.password2_entry = QLineEdit()
        self.password2_entry.setEchoMode(QLineEdit.Password)
        self.password2_entry.setFont(subheading_font)
        self.password2_entry.setMaximumWidth(800)
        entry_layout.addRow(password2_label, self.password2_entry)

        # Login button
        self.save_button = QPushButton('Save')
        self.save_button.setFont(subheading_font)
        self.save_button.clicked.connect(self.save_cred)

        # Error Message
        self.error_message = QLabel('')
        self.error_message.setAlignment(Qt.AlignCenter)

        entry = QHBoxLayout()
        entry.addWidget(space)
        entry.addLayout(entry_layout)
        layout = QVBoxLayout()
        layout.addLayout(entry)
        layout.addWidget(self.save_button)
        layout.addWidget(self.error_message)
        self.setLayout(layout)

    def save_cred(self):
        check = self.check_master()
        user = self.check_user()
        if self.password_entry.text() == self.password2_entry.text():
            if check:
                if self.username_entry.text() and self.password_entry.text():
                    if user:
                        self.set_creds()
                    else:
                        self.error_message.setText('This user already exists')
                else:
                    self.error_message.setText('Username or Password is invalid')
            else:
                self.error_message.setText('Master Password Incorrect')
        else:
            self.error_message.setText('Passwords do not match')

    def set_creds(self):
        # Get user input for username and password
        username = self.username_entry.text()
        password = self.password_entry.text()

        with open('credentials.txt', 'a') as file:
            # Write the username and password to the file
            file.write(f'\nUsername: {username} Password: {password}')

        print("Credentials have been written to the file.")
        self.close()

    def check_master(self):
        # Get user input for the credentials to search
        search_master = self.master_entry.text()

        with open('credentials.txt', 'r') as file:
            # Iterate through each line in the file
            for line in file:
                # Check if the current line exactly matches the search credentials
                if all(word in line for word in target_words):
                    return True
            return False

    def check_user(self):
        # Get user input for the credentials to search
        search_username = self.username_entry.text()
        with open('credentials.txt', 'r') as file:
            # Iterate through each line in the file
            for line in file:
                # Check if the current line exactly matches the search credentials
                if line.strip() == f'Username: {search_username}':
                    return False
        return True

    def close(self):
        self.master_entry.setText('')
        self.username_entry.setText('')
        self.password_entry.setText('')
        self.password2_entry.setText('')
        self.reject()
