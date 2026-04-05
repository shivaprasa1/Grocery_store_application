import mysql.connector

print("=== Aiven Database Setup ===")
print("Please enter your Aiven connection details.")
host = input("Host (e.g., mysql-xyz.aivencloud.com): ").strip()
port = input("Port (usually 25060): ").strip()
user = input("User (usually avnadmin): ").strip()
password = input("Password: ").strip()
database = input("Database Name (usually defaultdb): ").strip()

try:
    print("\nConnecting to Aiven MySQL...")
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()
    print("Successfully connected!")

    print("Running schema.sql to create tables...")
    with open('schema.sql', 'r') as file:
        schema_queries = file.read().split(';')
        
        for query in schema_queries:
            if query.strip():
                cursor.execute(query)
                conn.commit()
    
    print("\nSUCCESS! Your tables and initial data have been successfully created on Aiven!")
    print("\n--- NEXT STEP ---")
    print("Go to your Render account (dashboard.render.com).")
    print("Add the following Environment Variables to your Service:")
    print(f"DB_HOST = {host}")
    print(f"DB_USER = {user}")
    print(f"DB_PASSWORD = {password}")
    print(f"DB_NAME = {database}")

except Exception as e:
    print(f"\nError: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
