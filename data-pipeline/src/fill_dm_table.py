"""
Module for filling Data Mart table by calling SQL DM function
"""
import sys
import os

# Ensure project root is in path
if os.path.dirname(os.path.dirname(os.path.dirname(__file__))) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import psycopg2
from datetime import datetime, date
import config


def fill_dm_table(start_date, end_date, db_config=None):
    """
    Call PostgreSQL DM function to transform and load data into data mart table
    
    Args:
        start_date (str or date): Start date for DM processing (format: 'YYYY-MM-DD')
        end_date (str or date): End date for DM processing (format: 'YYYY-MM-DD')
        db_config (dict): Database configuration (optional)
        
    Returns:
        int: Number of rows processed
    """
    if db_config is None:
        db_config = config.DB_CONFIG
    
    # Convert string dates to date objects if needed
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    conn = None
    cursor = None
    
    try:
        # Connect to database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Call DM function
        function_call = f"""
            SELECT {config.SCHEMA_NAME}.fn_dm_data_load(%s, %s)
        """
        
        cursor.execute(function_call, (start_date, end_date))
        result = cursor.fetchone()
        rows_processed = result[0] if result else 0
        
        conn.commit()
        
        print(f"DM function executed successfully. Rows processed: {rows_processed}")
        
        return rows_processed
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error executing DM function: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        raise
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
