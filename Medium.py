import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .master('local[*]') \
    .config("spark.driver.memory", "15g") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .config("spark.driver.host", "127.0.0.1") \
    .appName('my-app') \
    .getOrCreate()

df = spark.read.csv('/Users/maverix/Desktop/mon/pyspark/data/winemag-data_first150k.csv',header=True)
df.show()
df.select("points", "price").show(20, truncate=False)
df = (
    df
    .withColumn("points_clean",
                F.regexp_replace(F.trim(F.col("points")), r"[^0-9.\-]", ""))
    .withColumn("price_clean",
                F.regexp_replace(F.trim(F.col("price")), r"[^0-9.\-]", ""))
    .withColumn("points", F.col("points_clean").cast("double"))
    .withColumn("price",  F.col("price_clean").cast("double"))
    .drop("points_clean", "price_clean")
)
#count uquie countries
df.select("country").distinct().count()
#average points by country
avg_points_by_country = (
    df.groupBy("country")
    .agg(F.round(F.avg("points"), 2).alias("avg_points"))
    .orderBy(F.desc("avg_points"))
)
avg_points_by_country.show(10, truncate=False)