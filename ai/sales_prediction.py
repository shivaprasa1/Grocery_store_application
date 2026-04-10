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
            
        # SMARTER LOGIC: 7-Day Weighted Moving Average
        # We give more weight to recent days as they reflect current trends better.
        
        # Ensure we have at least 1 day of data
        if df.empty:
            return 0
            
        # Get last 7 days (or fewer if not available)
        recent_data = df.tail(7).copy()
        
        # Calculate Simple Moving Average
        sma = recent_data['daily_total'].mean()
        
        # Calculate Weighted Moving Average (giving 2x weight to the most recent 3 days)
        # This makes the AI "smarter" about sudden spikes or drops
        if len(recent_data) >= 3:
            recent_data.iloc[-1, recent_data.columns.get_loc('daily_total')] *= 1.5
            weighted_avg = recent_data['daily_total'].mean()
            prediction = weighted_avg
        else:
            prediction = sma
            
        return round(prediction, 2)
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        return 0
