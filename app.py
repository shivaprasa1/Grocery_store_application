from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_connection import get_sql_connection
from dao import products_dao, orders_dao, user_dao
from ai.sales_prediction import train_and_predict_sales
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey123') # Change this in production

# Note: We open connection locally in methods to avoid thread issues,
# but for simplicity let's initialize it here or inside routes.
# Best practice is to open and close connection per request, so let's do that.

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        connection = get_sql_connection()
        user = user_dao.get_user_by_username(connection, username)
        connection.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'staff')
        
        connection = get_sql_connection()
        existing_user = user_dao.get_user_by_username(connection, username)
        
        if existing_user:
            connection.close()
            return render_template('register.html', error='Username already exists')
        
        hashed_pw = generate_password_hash(password)
        user_dao.insert_new_user(connection, username, hashed_pw, role)
        connection.close()
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'), role=session.get('role'))

@app.route('/getProducts', methods=['GET'])
def get_products():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    connection = get_sql_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    products = products_dao.get_all_products(connection)
    connection.close()
    return jsonify({'products': products})

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Permission denied. Admins only.'}), 403
    connection = get_sql_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
        
    try:
        request_payload = request.get_json()
        product_id = products_dao.insert_new_product(connection, request_payload)
        connection.close()
        return jsonify({'product_id': product_id})
    except Exception as e:
        connection.rollback()
        connection.close()
        return jsonify({'error': str(e)}), 500

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Permission denied. Admins only.'}), 403
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
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
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
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    connection = get_sql_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
        
    orders = orders_dao.get_all_orders(connection)
    connection.close()
    return jsonify({'orders': orders})

@app.route('/predictSales', methods=['GET'])
def predict_sales():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    prediction = train_and_predict_sales()
    return jsonify({'predicted_sales': prediction})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
