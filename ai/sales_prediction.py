import pandas as pd
from sklearn.linear_model import LinearRegression
from database.db_connection import get_sql_connection

def train_and_predict_sales():
    connection = get_sql_connection()
    if not connection:
        return 0
        
    query = "SELECT DATE(date) as order_date, SUM(total) as daily_total FROM orders GROUP BY DATE(date) ORDER BY DATE(date)"
    
    try:
        df = pd.read_sql(query, connection)
        connection.close()
        
        if df.empty or len(df) < 2:
            return 0 # Not enough data to predict
            
        # Feature engineering: converting dates to numerical format for simple linear regression
        df['days_since_start'] = (pd.to_datetime(df['order_date']) - pd.to_datetime(df['order_date'].min())).dt.days
        
        X = df[['days_since_start']]
        y = df['daily_total']
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict for the next day
        next_day = df['days_since_start'].max() + 1
        prediction = model.predict([[next_day]])
        
        return max(0, round(prediction[0], 2)) # Ensure it's not negative
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        return 0
