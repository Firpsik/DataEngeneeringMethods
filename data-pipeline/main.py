"""
Main entry point for ETL pipeline
"""
import sys
import os

# Add src directory and project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from etl import etl


if __name__ == '__main__':
    try:
        result = etl()
        print("\nETL execution result:", result)
        sys.exit(0)
    except Exception as e:
        print(f"\nETL failed with error: {e}")
        sys.exit(1)
