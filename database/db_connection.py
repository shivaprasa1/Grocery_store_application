import mysql.connector
import os

def get_sql_connection():
    try:
        # For Aiven and other managed DBs, we often need SSL.
        # Most modern clients handle this automatically, but we can be explicit.
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            port=int(os.environ.get('DB_PORT', 3306)),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', 'root'),
            database=os.environ.get('DB_NAME', 'grocery_store'),
            ssl_disabled=False  # Ensure SSL is NOT disabled for remote connections
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None
