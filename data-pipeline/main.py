"""
Main entry point for ETL pipeline
"""
import sys
import os

# Add src directory and project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from etl import etl
from init_postgres import init_postgres_schema
from fill_dm_table import fill_dm_table
from load_to_mysql import load_to_mysql
import config


if __name__ == '__main__':
    try:
        # Step 1: Run ETL (extract, transform, load to structured table)
        print("\n" + "="*80)
        print("STEP 1: Running ETL Pipeline")
        print("="*80)
        result = etl()
        print("\nETL execution result:", result)
        
        # Step 2: Initialize PostgreSQL DWH Schema
        print("\n" + "="*80)
        print("STEP 2: Initializing PostgreSQL DWH")
        print("="*80)
        init_postgres_schema()
        
        # Step 3: Fill Data Mart (load to t_dm_task with dimension tables)
        print("\n" + "="*80)
        print("STEP 3: Filling Data Mart (PostgreSQL)")
        print("="*80)
        dm_rows = fill_dm_table(config.START_DATE, config.END_DATE)
        print(f"\nData Mart filled: {dm_rows} rows")
        
        # Step 4: Load to MySQL
        print("\n" + "="*80)
        print("STEP 4: Loading to MySQL")
        print("="*80)
        mysql_rows = load_to_mysql(config.START_DATE, config.END_DATE)
        print(f"\nMySQL loaded: {mysql_rows} rows")
        
        # Summary
        print("\n" + "="*80)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("="*80)
        print(f"[OK] ETL: {result['records_processed']} rows in structured table")
        print(f"[OK] Data Mart: {dm_rows} rows in PostgreSQL")
        print(f"[OK] MySQL: {mysql_rows} rows loaded")
        print("="*80 + "\n")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\nPipeline failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
