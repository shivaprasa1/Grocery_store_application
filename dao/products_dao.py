def get_all_products(connection):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM products"
    cursor.execute(query)
    response = []
    for row in cursor:
        response.append(row)
    cursor.close()
    return response

def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = "INSERT INTO products (name, unit, price_per_unit) VALUES (%s, %s, %s)"
    data = (product['name'], product['unit'], product['price_per_unit'])
    cursor.execute(query, data)
    connection.commit()
    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = "DELETE FROM products WHERE product_id = %s"
    cursor.execute(query, (product_id,))
    connection.commit()
    return cursor.lastrowid
