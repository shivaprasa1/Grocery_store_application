from database.db_connection import get_sql_connection
from dao import user_dao
from werkzeug.security import generate_password_hash
import sys

def create_initial_admin():
    connection = get_sql_connection()
    if not connection:
        print("Error: Could not connect to database.")
        return

    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    
    # Check if user already exists
    existing_user = user_dao.get_user_by_username(connection, username)
    if existing_user:
        print(f"Error: User '{username}' already exists.")
        connection.close()
        return

    hashed_pw = generate_password_hash(password)
    user_id = user_dao.insert_new_user(connection, username, hashed_pw, 'admin')
    
    print(f"Success! Admin user '{username}' created with ID: {user_id}")
    connection.close()

if __name__ == "__main__":
    create_initial_admin()
