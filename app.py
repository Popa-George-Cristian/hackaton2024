import mysql.connector
import customtkinter as ctk
import os
import admin, user
from db import connect_to_db

# Database connection function
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change to your MySQL server's host
            user='root',  # Your MySQL username
            password='12345',  # Your MySQL password
            database='HACKATON2024'  # Your MySQL database name
        )
        print("Connected to the database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

class InterfaceLogin():
    def __init__(self, window, switch_page_callback):
        self.window = window
        self.switch_page_callback = switch_page_callback
        self.mainFrame = None
        self.loginAuth()

    def loginAuth(self):
        # Main frame for login
        self.mainFrame = ctk.CTkFrame(self.window, corner_radius=10, fg_color='white')
        self.mainFrame.pack(fill='both', expand=True)

        # Title container with color
        self.containerTitle = ctk.CTkFrame(self.mainFrame, corner_radius=5, fg_color='#2586d5')
        self.containerTitle.pack(fill='x', padx=20, pady=20)

        self.titleFrame = ctk.CTkLabel(self.containerTitle, text='Login System', font=("Arial", 20), anchor='center', text_color='white')
        self.titleFrame.pack(padx=10, pady=10)

        # Input fields for username and password
        self.containerMenu = ctk.CTkFrame(self.mainFrame, corner_radius=5, fg_color='transparent')
        self.containerMenu.pack(fill='both', expand=True)

        self.containerInput = ctk.CTkFrame(self.containerMenu, corner_radius=10, fg_color='#2586d5')
        self.containerInput.pack(padx=30, pady=20, expand=True)

        self.inputFrame1 = ctk.CTkFrame(self.containerInput, corner_radius=5, fg_color='transparent')
        self.inputFrame1.pack(padx=20, pady=15, fill='x')

        self.usernameLabel = ctk.CTkLabel(self.inputFrame1, text='Username:', font=("Arial", 14), text_color='white')
        self.usernameLabel.pack(side='left', padx=10)

        self.usernameInput = ctk.CTkEntry(self.inputFrame1, width=250, font=("Arial", 14), height=40, border_color='#2586d5')
        self.usernameInput.pack(side='left', padx=10)

        self.inputFrame2 = ctk.CTkFrame(self.containerInput, corner_radius=5, fg_color='transparent')
        self.inputFrame2.pack(padx=20, pady=15, fill='x')

        self.passwordLabel = ctk.CTkLabel(self.inputFrame2, text='Password:', font=("Arial", 14), text_color='white')
        self.passwordLabel.pack(side='left', padx=10)

        self.passwordInput = ctk.CTkEntry(self.inputFrame2, width=250, show="*", font=("Arial", 14), height=40, border_color='#2586d5')
        self.passwordInput.pack(side='left', padx=10)

        self.buttonLogin = ctk.CTkButton(self.containerInput, text='Login', command=self.handleLogin, width=150, font=("Arial", 16), fg_color='#4CAF50', hover_color='#45a049')
        self.buttonLogin.pack(pady=20)

        self.errorLabel = None

    def handleLogin(self):
        username = self.usernameInput.get()
        password = self.passwordInput.get()

        print(f"Login attempt with username: {username} and password: {password}")
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = "SELECT mode FROM loginauth WHERE nume = %s AND parola = %s"
            try:
                cursor.execute(query, (username, password))
                result = cursor.fetchone()
                print(f"Query result: {result}") 

                connection.close()

                if result:
                    mode = result[0]
                    if mode == 1: #Admin
                        self.switch_page_callback(2)
                    elif mode == 0: #Operator
                        print("Mode is 0, executing another script.")
                        self.switch_page_callback(1)
                    else:
                        print(f"Unexpected mode value: {mode}.")
                else:
                    print("Invalid credentials.")
                    self.show_error_message("Invalid credentials. Please try again.")
            except mysql.connector.Error as err:
                print(f"Database query error: {err}")
                self.show_error_message("Error querying the database.")
        else:
            self.show_error_message("Database connection failed.")

    def execute_script(self, script_name):
        try:
            script_path = os.path.join(os.path.dirname(__file__), script_name)
            os.system(f'python "{script_path}"')
        except Exception as e:
            print(f"Error executing script: {e}")
            self.show_error_message(f"Error executing script: {script_name}")

    def show_error_message(self, message):
        if self.errorLabel:
            self.errorLabel.destroy()

        self.errorLabel = ctk.CTkLabel(self.containerInput, text=message, font=("Arial", 14), text_color='red')
        self.errorLabel.pack(pady=10)

class Main():
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title('Login')
        self.window.geometry('800x480')
        self.window.resizable(False, False)

        self.page = 0
        self.switchPage(self.page)
        self.window.mainloop()

    def switchPage(self, page):
        for widget in self.window.winfo_children():
            widget.destroy()

        if page == 0:
            InterfaceLogin(self.window, self.switchPage)
        elif page == 1:
            user.InterfaceMonitor(self.window, self.switchPage)
        elif page == 2:
            admin.InterfaceAdmin(self.window, self.switchPage)

main = Main()
