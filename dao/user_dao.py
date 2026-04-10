
def get_user_by_username(connection, username):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    return user

def insert_new_user(connection, username, hashed_password, role='staff'):
    cursor = connection.cursor()
    query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
    data = (username, hashed_password, role)
    cursor.execute(query, data)
    connection.commit()
    user_id = cursor.lastrowid
    cursor.close()
    return user_id
