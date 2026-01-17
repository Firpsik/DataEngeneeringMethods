"""
Module for filling structured table by calling SQL ETL function
"""
import sys
import os

# Ensure project root is in path
if os.path.dirname(os.path.dirname(os.path.dirname(__file__))) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import psycopg2
from datetime import datetime, date
import config


def fill_structured_table(start_date, end_date, db_config=None):
    """
    Call PostgreSQL ETL function to transform and load data into structured table
    
    Args:
        start_date (str or date): Start date for ETL processing (format: 'YYYY-MM-DD')
        end_date (str or date): End date for ETL processing (format: 'YYYY-MM-DD')
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
        
        # Create ETL function if not exists
        with open('sql/dds/s_sql_dds/function/fn_etl_data_load.sql', 'r', encoding='utf-8') as f:
            cursor.execute(f.read())
        conn.commit()
        
        # Call ETL function
        function_call = f"""
            SELECT {config.SCHEMA_NAME}.{config.ETL_FUNCTION_NAME}(%s, %s)
        """
        
        cursor.execute(function_call, (start_date, end_date))
        result = cursor.fetchone()
        rows_processed = result[0] if result else 0
        
        conn.commit()
        
        print(f"ETL function executed successfully. Rows processed: {rows_processed}")
        
        return rows_processed
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error executing ETL function: {e}")
        raise
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
