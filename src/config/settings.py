"""
Configuration settings for the PySpark ETL project.
"""

# Spark configuration
SPARK_CONFIG = {
    "spark.app.name": "PySpark ETL Pipeline",
    "spark.driver.bindAddress": "127.0.0.1",
    "spark.sql.shuffle.partitions": "2",
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
}

# File paths
DATA_DIR = "data"
OUTPUT_DIR = "output"

# ETL specific settings
ETL_CONFIG = {
    "input_file": f"{DATA_DIR}/employees.csv",
    "output_dir": f"{OUTPUT_DIR}/transformed_employees",
    "output_format": "parquet",  # parquet, csv, json
}

# Salary thresholds for categorization
SALARY_THRESHOLDS = {
    "high": 80000,
    "medium": 60000,
}

# Age thresholds for grouping
AGE_THRESHOLDS = {
    "young": 30,
    "middle": 40,
}