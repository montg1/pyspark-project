"""
ETL (Extract, Transform, Load) pipeline for wine reviews data processing.
"""

from pyspark.sql.functions import col, when, avg, round as spark_round, count
from src.utils.spark_utils import (
    create_spark_session,
    ensure_directory,
    validate_file_exists,
)
from src.config.settings import ETL_CONFIG, POINTS_THRESHOLDS, PRICE_THRESHOLDS


def extract_data(spark, file_path):
    """
    Extract data from CSV file.

    Args:
        spark (SparkSession): Active Spark session
        file_path (str): Path to the input CSV file

    Returns:
        DataFrame: Raw data from CSV

    Raises:
        FileNotFoundError: If input file doesn't exist
    """
    validate_file_exists(file_path)
    return spark.read.csv(file_path, header=True, inferSchema=True)


def transform_data(df):
    """
    Transform the wine reviews data: clean, add calculations, and filter.

    Args:
        df (DataFrame): Raw wine reviews data

    Returns:
        DataFrame: Transformed wine data
    """
    # Clean data: handle missing values and filter out invalid entries
    df_clean = df.dropna(subset=["country", "points", "price", "variety"])

    # Add quality category based on points
    df_transformed = df_clean.withColumn(
        "Quality_Category",
        when(col("points") >= POINTS_THRESHOLDS["excellent"], "Excellent")
        .when(col("points") >= POINTS_THRESHOLDS["good"], "Good")
        .when(col("points") >= POINTS_THRESHOLDS["average"], "Average")
        .otherwise("Below Average"),
    )

    # Add price category
    df_transformed = df_transformed.withColumn(
        "Price_Category",
        when(col("price") >= PRICE_THRESHOLDS["premium"], "Premium")
        .when(col("price") >= PRICE_THRESHOLDS["mid_range"], "Mid-Range")
        .otherwise("Budget"),
    )

    # Calculate country statistics
    country_stats = df_transformed.groupBy("country").agg(
        spark_round(avg("points"), 2).alias("Country_Avg_Points"),
        spark_round(avg("price"), 2).alias("Country_Avg_Price"),
        count("*").alias("Wine_Count"),
    )

    # Join back to main dataframe
    df_final = df_transformed.join(country_stats, "country")

    # Filter: keep only wines above country average points
    df_filtered = df_final.filter(col("points") > col("Country_Avg_Points"))

    return df_filtered


def load_data(df, output_path, format="parquet"):
    """
    Load transformed data to specified location.

    Args:
        df (DataFrame): Transformed data to save
        output_path (str): Output directory path
        format (str): Output format (parquet, csv, json)

    Raises:
        ValueError: If format is not supported
    """
    ensure_directory(output_path)

    # Write data based on format
    if format == "parquet":
        df.write.mode("overwrite").parquet(output_path)
    elif format == "csv":
        df.write.mode("overwrite").csv(output_path, header=True)
    elif format == "json":
        df.write.mode("overwrite").json(output_path)
    else:
        raise ValueError(f"Unsupported format: {format}")

    print(f"Data loaded to {output_path} in {format} format")


def download_kaggle_dataset(dataset_path="data", dataset_name="zynicide/wine-reviews"):
    """
    Download dataset from Kaggle using direct URL download as fallback.

    Args:
        dataset_path (str): Path to download the dataset
        dataset_name (str): Kaggle dataset name

    Returns:
        bool: True if download successful, False otherwise
    """
    try:
        import subprocess
        import os
        import urllib.request
        import zipfile

        print(f"📥 Downloading {dataset_name} from Kaggle...")

        # Ensure data directory exists
        os.makedirs(dataset_path, exist_ok=True)

        # Try using Python kaggle API first
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi
            api = KaggleApi()
            api.authenticate()

            # Download the dataset
            api.dataset_download_files(dataset_name, path=dataset_path, unzip=True)
            print("✅ Dataset downloaded and extracted successfully via API!")
            return True

        except Exception as api_error:
            print(f"⚠️  Kaggle API failed: {str(api_error)}")
            print("🔄 Trying direct URL download...")

        # Fallback: Direct URL download (works without authentication for public datasets)
        try:
            kaggle_url = f"https://www.kaggle.com/api/v1/datasets/download/{dataset_name}"
            zip_path = os.path.join(dataset_path, "wine-reviews.zip")

            print(f"📡 Downloading from: {kaggle_url}")
            urllib.request.urlretrieve(kaggle_url, zip_path)
            print("✅ Dataset downloaded successfully via direct URL!")

            # Extract the zip file
            print("📦 Extracting dataset...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(dataset_path)
            print("✅ Dataset extracted successfully!")

            # Clean up zip file
            os.remove(zip_path)
            return True

        except Exception as url_error:
            print(f"❌ Direct download failed: {str(url_error)}")
            return False

    except Exception as e:
        print(f"❌ Download failed: {str(e)}")
        return False


def run_etl_pipeline(input_path=None, output_path=None, spark_config=None):
    """
    Run the complete ETL pipeline.

    Args:
        input_path (str): Path to input file (uses config default if None)
        output_path (str): Path to output directory (uses config default if None)
        spark_config (dict): Additional Spark configuration
    """
    # Auto-detect input file: use full dataset if available, download if possible, otherwise sample data
    if input_path is None:
        import os
        full_dataset = ETL_CONFIG["full_dataset"]
        sample_dataset = ETL_CONFIG["input_file"]

        if os.path.exists(full_dataset):
            input_file = full_dataset
            print(f"📊 Using full wine reviews dataset: {full_dataset}")
        else:
            print(f"📊 Full dataset not found: {full_dataset}")
            print("🔄 Attempting to download from Kaggle...")

            # Try to download the dataset
            if download_kaggle_dataset():
                # Check if download was successful
                if os.path.exists(full_dataset):
                    input_file = full_dataset
                    print(f"📊 Using downloaded wine reviews dataset: {full_dataset}")
                else:
                    input_file = sample_dataset
                    print(f"📊 Download completed but file not found, using sample data: {sample_dataset}")
            else:
                input_file = sample_dataset
                print(f"📊 Download failed, using sample wine data: {sample_dataset}")
                print("💡 Tip: Install kaggle CLI and configure API key for automatic downloads!")
    else:
        input_file = input_path

    output_dir = output_path or ETL_CONFIG["output_dir"]
    output_format = ETL_CONFIG["output_format"]

    spark = create_spark_session(extra_config=spark_config)

    try:
        print("Starting ETL pipeline...")
        print(f"Input: {input_file}")
        print(f"Output: {output_dir}")

        # Extract
        print("📥 Extracting data...")
        raw_df = extract_data(spark, input_file)
        print(f"✅ Extracted {raw_df.count()} records")

        # Transform
        print("🔄 Transforming data...")
        transformed_df = transform_data(raw_df)
        print(f"✅ Transformed to {transformed_df.count()} records")

        # Load
        print("📤 Loading data...")
        load_data(transformed_df, output_dir, output_format)

        # Show sample results
        print("\n📊 Sample of transformed data:")
        transformed_df.show(5)

        print("\n🎉 ETL pipeline completed successfully!")

    except Exception as e:
        print(f"❌ ETL pipeline failed: {str(e)}")
        raise
    finally:
        spark.stop()
