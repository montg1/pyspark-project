#!/usr/bin/env python3
"""
Script to read and display the transformed ETL output.
Usage: python scripts/read_output.py
"""

import sys
import os

# Add the parent directory to sys.path to import src modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

try:
    from src.utils.spark_utils import create_spark_session
    from src.config.settings import ETL_CONFIG
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)


def main():
    """Main function to read and display transformed data."""
    spark = create_spark_session("Read Transformed Data")

    try:
        output_dir = ETL_CONFIG["output_dir"]

        if not os.path.exists(output_dir):
            print(f"❌ Output directory not found: {output_dir}")
            print("Run the ETL pipeline first: python -m src.main")
            return

        df = spark.read.parquet(output_dir)

        print("📊 Transformed Data:")
        df.show()

        print(f"\n📈 Total records: {df.count()}")
        print(f"📋 Columns: {df.columns}")

        # Show some statistics
        print("\n📊 Country Summary:")
        df.groupBy("country").count().orderBy("count", ascending=False).show(10)

        print("\n⭐ Quality Categories:")
        df.groupBy("Quality_Category").count().orderBy("count", ascending=False).show()

        print("\n💰 Price Categories:")
        df.groupBy("Price_Category").count().orderBy("count", ascending=False).show()

        print("\n🍷 Top Varieties:")
        df.groupBy("variety").count().orderBy("count", ascending=False).show(10)

    except Exception as e:
        print(f"❌ Error reading data: {str(e)}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
