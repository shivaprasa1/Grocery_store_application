from flask import Flask, render_template, request, jsonify
from database.db_connection import get_sql_connection
from dao import products_dao, orders_dao
from ai.sales_prediction import train_and_predict_sales

app = Flask(__name__)

# Note: We open connection locally in methods to avoid thread issues,
# but for simplicity let's initialize it here or inside routes.
# Best practice is to open and close connection per request, so let's do that.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getProducts', methods=['GET'])
def get_products():
    connection = get_sql_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    products = products_dao.get_all_products(connection)
    connection.close()
    return jsonify({'products': products})

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    connection = get_sql_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
        
    request_payload = request.get_json()
    product_id = products_dao.insert_new_product(connection, request_payload)
    connection.close()
    return jsonify({'product_id': product_id})

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    connection = get_sql_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
        
    try:
        request_payload = request.get_json()
        product_id = products_dao.delete_product(connection, request_payload['product_id'])
        connection.close()
        return jsonify({'product_id': product_id})
    except Exception as e:
        connection.rollback()
        connection.close()
        # Cleanly capture foreign key integerity error for the frontend
        if "foreign key constraint fails" in str(e).lower():
            return jsonify({'error': 'Cannot delete this product because it exists in past historical orders. Deleting it would corrupt past financial receipts!'}), 400
        return jsonify({'error': str(e)}), 500

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    connection = get_sql_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
        
    try:
        request_payload = request.get_json()
        order_id = orders_dao.insert_order(connection, request_payload)
        connection.close()
        return jsonify({'order_id': order_id})
    except Exception as e:
        connection.rollback()
        connection.close()
        return jsonify({'error': str(e)}), 500

@app.route('/getOrders', methods=['GET'])
def get_orders():
    connection = get_sql_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
        
    orders = orders_dao.get_all_orders(connection)
    connection.close()
    return jsonify({'orders': orders})

@app.route('/predictSales', methods=['GET'])
def predict_sales():
    prediction = train_and_predict_sales()
    return jsonify({'predicted_sales': prediction})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
