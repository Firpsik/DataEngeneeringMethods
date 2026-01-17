"""
Main ETL orchestration module
"""
import sys
import os

# Ensure project root is in path
if os.path.dirname(os.path.dirname(os.path.dirname(__file__))) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from get_dataset import get_dataset
from load_data_to_db import load_data_to_db, create_tables
from fill_structured_table import fill_structured_table
import config


def etl():
    """
    Top-level ETL function that orchestrates the entire pipeline
    
    This function performs:
    1. Generates synthetic dataset with anomalies
    2. Loads data to unstructured table in PostgreSQL
    3. Calls SQL function to transform and load data into structured table
    
    Returns:
        dict: Summary of ETL execution
    """
    print("=" * 80)
    print("Starting ETL Pipeline")
    print("=" * 80)
    
    try:
        # Step 1: Generate dataset
        print("\nStep 1: Generating synthetic dataset...")
        df = get_dataset(num_records=config.NUM_RECORDS)
        print(f"Dataset shape: {df.shape}")
        
        # Step 2: Create tables
        print("\nStep 2: Creating database tables...")
        create_tables()
        
        # Step 3: Load data to unstructured table
        print("\nStep 3: Loading data to unstructured table...")
        rows_loaded = load_data_to_db(df)
        
        # Step 4: Fill structured table via SQL ETL function
        print("\nStep 4: Transforming and loading data to structured table...")
        rows_processed = fill_structured_table(
            start_date=config.START_DATE,
            end_date=config.END_DATE
        )
        
        # Summary
        summary = {
            'status': 'SUCCESS',
            'records_generated': len(df),
            'records_loaded': rows_loaded,
            'records_processed': rows_processed
        }
        
        print("\n" + "=" * 80)
        print("ETL Pipeline Completed Successfully")
        print("=" * 80)
        print(f"Records generated: {summary['records_generated']}")
        print(f"Records loaded to unstructured table: {summary['records_loaded']}")
        print(f"Records processed to structured table: {summary['records_processed']}")
        print("=" * 80)
        
        return summary
        
    except Exception as e:
        print(f"\n{'=' * 80}")
        print(f"ETL Pipeline Failed: {e}")
        print("=" * 80)
        raise
