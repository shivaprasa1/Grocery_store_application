# Grocery Store Management System

A full-stack web application built using Python Flask, MySQL, HTML, CSS, and Vanilla JavaScript.
It includes an AI module (Scikit-Learn) to predict next day's sales based on historical data.

## Project Structure
* `app.py` - Main Flask entry point.
* `database/db_connection.py` - MySQL connection setup.
* `dao/products_dao.py` & `dao/orders_dao.py` - Data Access Object layer for isolating database logic.
* `templates/index.html` - Premium UI built using standard Web practices.
* `static/css/style.css` - Custom styling focusing on aesthetics and responsiveness.
* `static/js/app.js` - Dynamic DOM manipulation and Fetch API client interactions.
* `ai/sales_prediction.py` - Linear Regression model to forecast sales.

## Pre-requisites
- Python 3.x
- MySQL Server

## Run Instructions

### 1. Database Setup
1. Open your MySQL client (e.g., MySQL Workbench or CLI).
2. Execute the `schema.sql` at the root of the project to build the database and necessary tables.
   (The commands included in `schema.sql` handle creating the `grocery_store` DB and all relations).
3. **Important**: Open `database/db_connection.py` and update the database password inside `get_sql_connection()` to match your local MySQL root password.

### 2. Install Dependencies
Open a terminal in the `d:\Resume_project` directory and install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Run the Backend
Start the Flask development server:

```bash
python app.py
```

### 4. Open the Application
Navigate in your web browser to:
`http://127.0.0.1:5000/`

You should now be able to add products, create new orders, and utilize the AI Sales Prediction tab!
