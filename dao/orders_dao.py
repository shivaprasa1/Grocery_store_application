import datetime

def insert_order(connection, order):
    cursor = connection.cursor()
    
    # Specify current time from Python explicitly 
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Insert order
    query = "INSERT INTO orders (customer_name, total, date) VALUES (%s, %s, %s)"
    data = (order['customer_name'], order['total'], now)
    cursor.execute(query, data)
    order_id = cursor.lastrowid
    
    # Insert order items
    order_details_query = ("INSERT INTO order_items "
                           "(order_id, product_id, quantity, price, total) "
                           "VALUES (%s, %s, %s, %s, %s)")
    
    order_details_data = []
    for item in order['order_items']:
        order_details_data.append([
            order_id,
            item['product_id'],
            item['quantity'],
            item['price_per_unit'],
            item['total']
        ])
        
    cursor.executemany(order_details_query, order_details_data)
    connection.commit()
    return order_id

def get_all_orders(connection):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM orders ORDER BY date DESC"
    cursor.execute(query)
    response = []
    for row in cursor:
        response.append(row)
    cursor.close()
    return response
