from pyspark.sql import SparkSession

def create_sample_dataframe(spark):
    """Create a sample DataFrame with Name and Age columns."""
    data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
    columns = ["Name", "Age"]
    return spark.createDataFrame(data, columns)

def main():
    # Create a Spark session
    spark = SparkSession.builder \
        .appName("PySpark Project") \
        .config("spark.driver.bindAddress", "127.0.0.1") \
        .getOrCreate()

    # Create a simple DataFrame
    df = create_sample_dataframe(spark)

    # Show the DataFrame
    df.show()

    # Stop the Spark session
    spark.stop()

if __name__ == "__main__":
    main()