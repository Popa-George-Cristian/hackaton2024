import mysql.connector

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
