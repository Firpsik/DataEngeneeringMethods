"""
Module for initializing PostgreSQL schema and tables
"""
import sys
import os

if os.path.dirname(os.path.dirname(os.path.dirname(__file__))) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import psycopg2
import config


def init_postgres_schema(db_config=None):
    """
    Initialize PostgreSQL schema and tables with autocommit
    """
    if db_config is None:
        db_config = config.DB_CONFIG
    
    conn = None
    cursor = None
    
    try:
        conn = psycopg2.connect(**db_config)
        conn.autocommit = True  # Important for DDL operations
        cursor = conn.cursor()
        
        # Create schema
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {config.SCHEMA_NAME}")
        
        # Create dimension tables
        dim_tables = [
            'sql/dds/s_sql_dds/table/d_customer.sql',
            'sql/dds/s_sql_dds/table/d_product_category.sql',
            'sql/dds/s_sql_dds/table/d_city.sql',
            'sql/dds/s_sql_dds/table/d_status.sql',
            'sql/dds/s_sql_dds/table/d_payment_method.sql',
            'sql/dds/s_sql_dds/table/t_dm_task.sql'
        ]
        
        for table_file in dim_tables:
            with open(table_file, 'r', encoding='utf-8') as f:
                cursor.execute(f.read())
        
        # Create DM function
        with open('sql/dds/s_sql_dds/function/fn_dm_data_load.sql', 'r', encoding='utf-8') as f:
            cursor.execute(f.read())
        
        # Create view
        with open('sql/dds/s_sql_dds/view/v_dm_task.sql', 'r', encoding='utf-8') as f:
            cursor.execute(f.read())
        
        print("PostgreSQL schema initialized successfully")
        
    except Exception as e:
        print(f"Error initializing PostgreSQL schema: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        raise
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
