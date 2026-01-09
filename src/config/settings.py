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
    "input_file": f"{DATA_DIR}/wine_reviews_sample.csv",  # Default to sample data
    "full_dataset": f"{DATA_DIR}/winemag-data-130k-v2.csv",  # Full dataset if available
    "output_dir": f"{OUTPUT_DIR}/transformed_wine_reviews",
    "output_format": "parquet",  # parquet, csv, json
}

# Wine quality thresholds for categorization
POINTS_THRESHOLDS = {
    "excellent": 95,
    "good": 85,
    "average": 75,
}

# Price thresholds for categorization
PRICE_THRESHOLDS = {
    "premium": 100,
    "mid_range": 50,
}
