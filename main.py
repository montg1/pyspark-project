from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder \
    .appName("PySpark Project") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()

# Create a simple DataFrame
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, columns)

# Show the DataFrame
df.show()

# Stop the Spark session
spark.stop()