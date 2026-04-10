# GSMS Portal v2.0 - Advanced Grocery Store Management 🌟

This is the upgraded version of the Grocery Store Management System, featuring enterprise-grade authentication, role-based access, and advanced AI forecasting.

## 🚀 Improvements from v1.0

We have taken this project from a basic CRUD app to a production-ready management portal:

### 1. 🔐 Secure Authentication System
- **Login/Logout**: Added a dedicated, beautiful login page with dark-mode aesthetics.
- **Password Hashing**: Implemented `werkzeug.security` to encrypt passwords. We no longer store plain text!
- **Session Management**: Secure Flask sessions handle user persistence.

### 2. 🛡️ Role-Based Access Control (RBAC)
- **Admin vs. Staff**: 
  - **Staff** can process orders and view the dashboard.
  - **Admins** have exclusive access to the **Inventory Management** panel to add or delete products.
- **Frontend Protection**: UI elements (like the "Manage Products" button) are hidden from non-admins using Jinja2 templates.
- **Backend Protection**: API routes are protected at the server level. Even if a user knows the URL, they cannot delete products without an Admin session.

### 3. 🇮🇳 Localization & Currency (NEW)
- **Indian Rupee (₹)**: Switched all currency notation from $ to ₹.
- **Dynamic Updates**: JS logic automatically handles ₹ formatting for grand totals and individual item prices.

### 4. 🔍 Real-Time Product Search
- Added a high-performance search bar in the new unified header.
- Users can filter products instantly as they type, both in the Inventory list and in the New Order dropdowns.

### 5. 📈 Advanced AI: 7-Day Moving Average
- **Upgraded from Linear Regression**: Linear models often fail with small inventory datasets.
- **Smart Weighted Average**: The system now uses a **Weighted Moving Average** that gives more importance to the most recent 3 days of sales, capturing current trends more accurately than a simple line-of-best-fit.

### 6. 🎨 Premium & Responsive UI
- **Mobile Friendly**: Added Media Queries to ensure the app looks great on both Smartphones and PCs.
- **Glassmorphism Header**: A completely redesigned top bar with user profile badges, logout links, and integrated search.
- **Alignment Fixes**: Resolved all layout issues with panels and tables to ensure a professional "Dashboard" feel.
- **Inter/Outfit Typography**: Switched to modern premium Google fonts.

---

## 🛠️ Updated Tech Stack
- **Backend**: Python Flask
- **Security**: Werkzeug Security (Hashing), Flask Sessions
- **AI/DS**: Pandas, Weighted Moving Average Logic
- **Database**: MySQL (Remote: Aiven / Local: MySQL Server)
- **Frontend**: HTML5, Vanilla JS (ES6+), Modern CSS3 with Flex/Grid

## 🏗️ New Project Structure
* `dao/user_dao.py` - **[NEW]** Data logic for handling users and roles.
* `templates/login.html` - **[NEW]** The premium login portal.
* `create_admin.py` - **[NEW]** Local setup tool to initialize the first admin.
* `fix_db.py` - **[NEW]** Automated migration script to build required tables.

---

## ⚙️ How to Update your Local Environment

If you are a developer moving from v1.0 to v2.0:

1. **Run the Database Migration**:
   ```bash
   python fix_db.py
   ```
   *This creates the `users` table and a default admin (`admin` / `admin123`).*

2. **Start the App**:
   ```bash
   python app.py
   ```

3. **Login and Explore**: Use the admin credentials to see the full power of the new Inventory panel.

---

*This project was improved to demonstrate mastery over web security, user experience design, and practical data science applications.*
