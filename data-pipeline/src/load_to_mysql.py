"""
Module for loading data to MySQL database
"""
import sys
import os

# Ensure project root is in path
if os.path.dirname(os.path.dirname(os.path.dirname(__file__))) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import psycopg2
import mysql.connector
from datetime import datetime, date
import config


def load_to_mysql(start_date, end_date, pg_config=None, mysql_config=None):
    """
    Load data from PostgreSQL view to MySQL staging table and then to final table
    
    Args:
        start_date (str or date): Start date
        end_date (str or date): End date
        pg_config (dict): PostgreSQL configuration (optional)
        mysql_config (dict): MySQL configuration (optional)
        
    Returns:
        int: Number of rows loaded to MySQL
    """
    if pg_config is None:
        pg_config = config.DB_CONFIG
    if mysql_config is None:
        mysql_config = config.MYSQL_CONFIG
    
    # Convert string dates to date objects if needed
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    pg_conn = None
    mysql_conn = None
    pg_cursor = None
    mysql_cursor = None
    
    try:
        # Connect to PostgreSQL
        pg_conn = psycopg2.connect(**pg_config)
        pg_conn.autocommit = True  # Read committed data
        pg_cursor = pg_conn.cursor()
        
        # Connect to MySQL
        mysql_conn = mysql.connector.connect(**mysql_config)
        mysql_cursor = mysql_conn.cursor()
        
        # Create MySQL schema if not exists
        mysql_cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {config.MYSQL_SCHEMA}")
        mysql_cursor.execute(f"USE {config.MYSQL_SCHEMA}")
        
        # Create MySQL tables
        mysql_tables = [
            'sql/dm/s_sql_dm/table/t_dm_stg_task.sql',
            'sql/dm/s_sql_dm/table/t_dm_task.sql'
        ]
        
        for table_file in mysql_tables:
            with open(table_file, 'r', encoding='utf-8') as f:
                # MySQL may have issues with multiple statements, execute one by one
                sql_content = f.read()
                for statement in sql_content.split(';'):
                    if statement.strip():
                        mysql_cursor.execute(statement)
        mysql_conn.commit()
        
        # Read data from PostgreSQL view
        pg_cursor.execute(f"""
            SELECT 
                record_id, customer_id, customer_name,
                product_category_id, product_category,
                city_id, city,
                status_id, status,
                payment_method_id, payment_method,
                amount, quantity, discount_percent,
                transaction_date, rating
            FROM {config.SCHEMA_NAME}.v_dm_task
            WHERE transaction_date BETWEEN %s AND %s
        """, (start_date, end_date))
        
        rows = pg_cursor.fetchall()
        
        if not rows:
            print("No data found in PostgreSQL view for the specified period")
            return 0
        
        # Clear staging table
        mysql_cursor.execute(f"""
            DELETE FROM {config.MYSQL_SCHEMA}.t_dm_stg_task
            WHERE transaction_date BETWEEN %s AND %s
        """, (start_date, end_date))
        
        # Insert data into MySQL staging table
        insert_query = f"""
            INSERT INTO {config.MYSQL_SCHEMA}.t_dm_stg_task (
                record_id, customer_id, customer_name,
                product_category_id, product_category,
                city_id, city,
                status_id, status,
                payment_method_id, payment_method,
                amount, quantity, discount_percent,
                transaction_date, rating
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        mysql_cursor.executemany(insert_query, rows)
        mysql_conn.commit()
        
        rows_loaded = len(rows)
        print(f"Successfully loaded {rows_loaded} rows to MySQL staging table")
        
        # Create MySQL procedure if not exists
        with open('sql/dm/s_sql_dm/function/fn_dm_data_stg_to_dm_load.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
            # Drop procedure if exists first
            mysql_cursor.execute("DROP PROCEDURE IF EXISTS s_sql_dm.fn_dm_data_stg_to_dm_load")
            mysql_cursor.execute(sql_content)
        mysql_conn.commit()
        
        # Call MySQL procedure to move data from staging to final table
        mysql_cursor.callproc('s_sql_dm.fn_dm_data_stg_to_dm_load', [start_date, end_date])
        
        # Fetch results
        for result in mysql_cursor.stored_results():
            print(result.fetchone()[0])
        
        mysql_conn.commit()
        
        print(f"Data successfully loaded to MySQL final table")
        
        return rows_loaded
        
    except Exception as e:
        if pg_conn:
            pg_conn.rollback()
        if mysql_conn:
            mysql_conn.rollback()
        print(f"Error loading to MySQL: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        raise
        
    finally:
        if pg_cursor:
            pg_cursor.close()
        if pg_conn:
            pg_conn.close()
        if mysql_cursor:
            mysql_cursor.close()
        if mysql_conn:
            mysql_conn.close()
