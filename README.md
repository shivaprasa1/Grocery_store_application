
# Grocery Store Management System 🌟

A full-stack web application built using Python Flask, MySQL, HTML, CSS, and Vanilla JavaScript.
It includes an AI module (Scikit-Learn) to predict next day's sales based on historical data.

## 🚀 Live Demo
View the deployed application: [https://grocery-store-application-jch2.onrender.com/](https://grocery-store-application-jch2.onrender.com/)

## ✨ Features
- 📋 **Product Management**: View all products, add new products (name, price, category), delete products (with foreign key protection to prevent data corruption).
- 🛒 **Order Management**: Place new orders by selecting products and quantities, view order history.
- 🤖 **AI Sales Prediction**: Get next-day sales forecast using Linear Regression model trained on historical order data.
- 🎨 **Responsive UI**: Single-page app with tabs, dynamic tables, forms, and modern styling (mobile-friendly).
- 🛡️ **Data Integrity**: SQL constraints and error handling (e.g., can't delete products in use).
- ☁️ **Cloud-Ready**: Deployed on Render with Aiven MySQL.

## 🏗️ Project Structure
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

## 🔄 Future Improvements & Roadmap
### High Priority 🚀
- 👤 User Authentication (Flask-Login/JWT): Login system, user roles (admin/customer).
- 🔍 Product Search/Filter/Sort: By name, price, category.
- 📦 Inventory Management: Track stock levels, low-stock alerts.

### Medium Priority ⚡
- 📊 Enhanced AI: Multiple models (Random Forest, Prophet), interactive charts (Chart.js), historical trends.
- 📝 Order Editing/Cancellation, detailed receipts.
- 📈 Dashboard: Analytics, sales reports, CSV export.

### Low Priority 🌱
- 🧪 Unit/Integration Tests (pytest).
- 📱 PWA Support (service worker, offline).
- 🐳 Docker Compose for local/cloud deploys.
- 🔄 Real-time updates (WebSockets/SSE).

Contributions welcome!

## ☁️ Cloud Deployment (Render & Aiven)

To share your application with the world, you can deploy it for free using **Render** (for hosting the Python Flask web server) and **Aiven** (for hosting the cloud MySQL database).

### Step 1: Set Up Cloud Database (Aiven)
1. Create a free MySQL database on [Aiven](https://aiven.io/). **No credit card is required.**
2. Once deployed, copy your connection details (Host, Port, User, Password).
3. Open your terminal locally in VS Code and run our remote setup script:
   ```bash
   python setup_remote_db.py
   ```
4. Paste your Aiven details when prompted. This will automatically execute the necessary SQL queries to build the tables in the cloud database.

### Step 2: Deploy Web Server (Render)
1. Push your code to a GitHub repository.
2. Log into [Render](https://dashboard.render.com/) and create a new **Web Service**.
3. Connect your GitHub repository.
4. Set the Build Command to: `pip install -r requirements.txt`
5. Set the Start Command to: `gunicorn app:app` (Gunicorn is required for production WSGI serving).
6. **Crucial Step - Environment Variables:** Go to the Environment tab of your Render service and add the following keys to link it to your Aiven Database:
   - `DB_HOST`: (Your Aiven Host)
   - `DB_PORT`: (Your Aiven Port)
   - `DB_USER`: `avnadmin`
   - `DB_PASSWORD`: (Your Aiven Password)
   - `DB_NAME`: `defaultdb`
7. Click **Deploy**! Your app is now live and talking to the cloud database.

### Step 3: Stop the "Sleep" Mode (Cron-job.org)
By default, Render's free tier puts your app to sleep after 15 minutes of inactivity, causing a 30-second delay when you first open the link. We solved this using a **Keep-Alive Hack**:
1. Go to [cron-job.org](https://cron-job.org/).
2. Create a free account and set up a new Cronjob.
3. Point it to your Render URL (e.g., `https://grocery-app.onrender.com`).
4. Set it to run every **14 minutes**.
5. **Result**: Your app will never go to sleep and will always open instantly! 🚀
