"""
Utility functions for PySpark ETL operations.
"""

import os
from pyspark.sql import SparkSession
from src.config.settings import SPARK_CONFIG


def create_spark_session(app_name=None, extra_config=None):
    """
    Create and configure a Spark session.

    Args:
        app_name (str): Application name for Spark session
        extra_config (dict): Additional Spark configuration

    Returns:
        SparkSession: Configured Spark session
    """
    config = SPARK_CONFIG.copy()
    if extra_config:
        config.update(extra_config)

    builder = SparkSession.builder.appName(
        app_name or config.get("spark.app.name", "PySpark ETL")
    )

    for key, value in config.items():
        builder = builder.config(key, value)

    return builder.getOrCreate()


def ensure_directory(path):
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        path (str): Directory path to create
    """
    os.makedirs(path, exist_ok=True)


def get_file_size_mb(file_path):
    """
    Get file size in MB.

    Args:
        file_path (str): Path to the file

    Returns:
        float: File size in MB
    """
    if os.path.exists(file_path):
        return os.path.getsize(file_path) / (1024 * 1024)
    return 0.0


def validate_file_exists(file_path):
    """
    Validate that a file exists.

    Args:
        file_path (str): Path to the file

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")


def get_spark_version():
    """
    Get the current Spark version.

    Returns:
        str: Spark version
    """
    spark = SparkSession.getActiveSession()
    if spark:
        return spark.version
    return "No active Spark session"
