"""
Configuration file for ETL pipeline
"""
import os

# PostgreSQL connection settings
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'etl_database'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

# Schema and table names
SCHEMA_NAME = 's_psql_dds'
UNSTRUCTURED_TABLE = 't_sql_source_unstructured'
STRUCTURED_TABLE = 't_sql_source_structured'
STRUCTURED_TABLE_COPY = 't_sql_source_structured_copy'

# ETL function name
ETL_FUNCTION_NAME = 'fn_etl_data_load'
ETL_FUNCTION_TEST_NAME = 'fn_etl_data_load_test'

# Data generation settings
NUM_RECORDS = 1000
START_DATE = '2023-01-01'
END_DATE = '2024-12-31'
