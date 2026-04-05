import mysql.connector

def get_sql_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root", # User must update this!
            database="grocery_store"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None
