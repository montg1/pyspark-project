"""
ETL (Extract, Transform, Load) pipeline for employee data processing.
"""

from pyspark.sql.functions import col, when, avg, round as spark_round
from src.utils.spark_utils import create_spark_session, ensure_directory, validate_file_exists
from src.config.settings import ETL_CONFIG, SALARY_THRESHOLDS, AGE_THRESHOLDS


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
    Transform the data: clean, add calculations, and filter.

    Args:
        df (DataFrame): Raw input data

    Returns:
        DataFrame: Transformed data
    """
    # Clean data: handle missing values
    df_clean = df.dropna()

    # Add calculated columns using configuration
    df_transformed = df_clean.withColumn(
        "Salary_Category",
        when(col("Salary") >= SALARY_THRESHOLDS["high"], "High")
        .when(col("Salary") >= SALARY_THRESHOLDS["medium"], "Medium")
        .otherwise("Low")
    )

    # Add age group
    df_transformed = df_transformed.withColumn(
        "Age_Group",
        when(col("Age") < AGE_THRESHOLDS["young"], "Young")
        .when(col("Age") < AGE_THRESHOLDS["middle"], "Middle")
        .otherwise("Senior")
    )

    # Calculate department averages
    dept_avg = df_transformed.groupBy("Department").agg(
        spark_round(avg("Salary"), 2).alias("Dept_Avg_Salary")
    )

    # Join back to main dataframe
    df_final = df_transformed.join(dept_avg, "Department")

    # Filter: keep only employees above department average
    df_filtered = df_final.filter(col("Salary") > col("Dept_Avg_Salary"))

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


def run_etl_pipeline(input_path=None, output_path=None, spark_config=None):
    """
    Run the complete ETL pipeline.

    Args:
        input_path (str): Path to input file (uses config default if None)
        output_path (str): Path to output directory (uses config default if None)
        spark_config (dict): Additional Spark configuration
    """
    # Use configuration defaults if not provided
    input_file = input_path or ETL_CONFIG["input_file"]
    output_dir = output_path or ETL_CONFIG["output_dir"]
    output_format = ETL_CONFIG["output_format"]

    spark = create_spark_session(extra_config=spark_config)

    try:
        print(f"Starting ETL pipeline...")
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