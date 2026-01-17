"""
Module for loading data to PostgreSQL database
"""
import sys
import os

# Ensure project root is in path
if os.path.dirname(os.path.dirname(os.path.dirname(__file__))) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import config


def load_data_to_db(df, db_config=None):
    """
    Load DataFrame to PostgreSQL unstructured table
    
    Args:
        df (pd.DataFrame): DataFrame to load
        db_config (dict): Database configuration (optional, uses config.DB_CONFIG by default)
        
    Returns:
        int: Number of rows loaded
    """
    if db_config is None:
        db_config = config.DB_CONFIG
    
    conn = None
    cursor = None
    
    try:
        # Connect to database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Create schema if not exists
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {config.SCHEMA_NAME}")
        
        # Truncate table before loading (clean start), only if table exists
        table_full_name = f"{config.SCHEMA_NAME}.{config.UNSTRUCTURED_TABLE}"
        cursor.execute(f"""
            DO $$ 
            BEGIN
                IF EXISTS (SELECT 1 FROM information_schema.tables 
                          WHERE table_schema = '{config.SCHEMA_NAME}' 
                          AND table_name = '{config.UNSTRUCTURED_TABLE}') THEN
                    TRUNCATE TABLE {table_full_name} CASCADE;
                END IF;
            END $$;
        """)
        
        # Prepare data for insertion
        # Replace NaN, infinity with None (NULL in SQL)
        import numpy as np
        df_clean = df.replace([np.inf, -np.inf], None)
        df_clean = df_clean.where(pd.notna(df_clean), None)
        
        # Convert numpy types to Python native types
        def convert_value(val):
            if val is None or pd.isna(val):
                return None
            elif isinstance(val, (np.integer, np.floating)):
                return val.item()  # Convert numpy types to Python native
            elif isinstance(val, np.bool_):
                return bool(val)
            else:
                return val
        
        columns = df_clean.columns.tolist()
        values = [[convert_value(v) for v in row] for row in df_clean.values]
        
        # Insert data
        insert_query = f"""
            INSERT INTO {table_full_name} 
            ({', '.join(columns)})
            VALUES %s
        """
        
        execute_values(cursor, insert_query, values)
        
        conn.commit()
        
        rows_loaded = len(df)
        print(f"Successfully loaded {rows_loaded} rows to {table_full_name}")
        
        return rows_loaded
        
    except Exception as e:
        if conn:
            conn.rollback()
        import traceback
        print(f"Error loading data to database: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        raise
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_tables(db_config=None):
    """
    Create necessary tables by executing SQL DDL scripts
    
    Args:
        db_config (dict): Database configuration
    """
    if db_config is None:
        db_config = config.DB_CONFIG
    
    conn = None
    cursor = None
    
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Read and execute table creation scripts
        with open('sql/dds/s_sql_dds/table/t_sql_source_unstructured.sql', 'r', encoding='utf-8') as f:
            cursor.execute(f.read())
        
        with open('sql/dds/s_sql_dds/table/t_sql_source_structured.sql', 'r', encoding='utf-8') as f:
            cursor.execute(f.read())
        
        conn.commit()
        print("Tables created successfully")
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error creating tables: {e}")
        raise
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
