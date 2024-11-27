import sys
from AUBoutique_client import send_command 
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QMessageBox
)
class EntryPage(QWidget): #first page
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout() #vertical layout
        header = QLabel("AUBoutique")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(header)
        login_button = QPushButton("Login") 
        register_button = QPushButton("Register") 
        login_button.clicked.connect(self.go_to_login) #login button redirects to login page
        register_button.clicked.connect(self.go_to_register) #register button redirects to registration page
        layout.addWidget(login_button)
        layout.addWidget(register_button)
        self.setLayout(layout)      
    
    def go_to_login(self):
        self.parent().set_page(LoginPage(self.parent()))
    def go_to_register(self):
        self.parent().set_page(RegistrationPage(self.parent()))
       
class LoginPage(QWidget): #login page
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        header = QLabel("Login")
        header.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(header)
        #login information input boxes
        self.username_input = QLineEdit().setPlaceholderText("Username") #enter username 
        self.password_input = QLineEdit().setPlaceholderText("Password") #enter password
        self.password_input.setEchoMode(QLineEdit.Password) #the setEchoMode allows to hide the characters
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.login)
        layout.addWidget(submit_button)
        self.setLayout(layout)
        
    def login(self): #login function implemented by login submit button
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            result = send_command("login", {"username": username, "password": password})
            if result.startswith("Login successful"):
                QMessageBox.information(self, "Success", "Login successful!")
                # Redirect to main page or dashboard
            else:
                QMessageBox.warning(self, "Error", result)
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            
class RegistrationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        header = QLabel("Register") #header
        header.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(header)
        #registration information input boxes
        self.name_input = QLineEdit().setPlaceholderText("Name")
        self.email_input = QLineEdit().setPlaceholderText("Email")
        self.username_input = QLineEdit().setPlaceholderText("Username")
        self.password_input = QLineEdit().setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.register)
        layout.addWidget(submit_button)
        self.setLayout(layout)
    
    def register(self):
        name = self.name_input.text() 
        email = self.email_input.text()
        username = self.username_input.text()
        password = self.username_input.text()
        if name and email and username and password:
            result = send_command("register", {"name": name, "email": email, "username": username, "password": password})
            if result == "Registration successful":
                QMessageBox.information(self, "Success", "Registration successful! Please log in")
                self.parent().set_page(EntryPage(self.parent))
            else:
                QMessageBox.warning(self, "Error", result)
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AUBoutique")
        self.setGeometry(300, 100, 400, 300)
        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.set_page(EntryPage(self))
    
    def set_page(self, page): #setting the entry point of application as EntryPage
        layout = QVBoxLayout()
        layout.addWidget(page)
        self.container.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
