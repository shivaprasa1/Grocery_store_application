from database.db_connection import get_sql_connection
from werkzeug.security import generate_password_hash

def setup_database():
    connection = get_sql_connection()
    if not connection:
        print("Failed to connect to database.")
        return

    cursor = connection.cursor()
    
    # Create users table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role ENUM('admin', 'staff') DEFAULT 'staff'
    )
    """
    try:
        cursor.execute(create_table_query)
        print("✅ Users table created successfully (or already exists).")
        
        # Add a default admin user
        username = "admin"
        password = "admin123"
        hashed_pw = generate_password_hash(password)
        
        # Only insert if doesn't exist
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                           (username, hashed_pw, 'admin'))
            connection.commit()
            print(f"✅ Default admin account created!")
            print(f"   User: {username}")
            print(f"   Pass: {password}")
        else:
            print("ℹ️ Admin user already exists.")
            
    except Exception as e:
        print(f"❌ Error setting up table: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    setup_database()
