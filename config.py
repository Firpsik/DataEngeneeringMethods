import os

# PostgreSQL connection settings
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'etl_database'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

# MySQL connection settings
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': os.getenv('MYSQL_PORT', '3306'),
    'database': os.getenv('MYSQL_DB', 'etl_mysql'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'root')
}

# Schema and table names
SCHEMA_NAME = 's_psql_dds'
MYSQL_SCHEMA = 's_sql_dm'
UNSTRUCTURED_TABLE = 't_sql_source_unstructured'
STRUCTURED_TABLE = 't_sql_source_structured'
DM_TABLE = 't_dm_task'

# ETL function name
ETL_FUNCTION_NAME = 'fn_etl_data_load'
DM_FUNCTION_NAME = 'fn_dm_data_load'

# Data generation settings
NUM_RECORDS = 1000
START_DATE = '2023-01-01'
END_DATE = '2024-12-31'
