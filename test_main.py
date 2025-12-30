import pytest
from pyspark.sql import SparkSession
from main import create_sample_dataframe


@pytest.fixture(scope="session")
def spark():
    """Create a Spark session for testing."""
    spark = SparkSession.builder \
        .appName("PySpark Test") \
        .config("spark.driver.bindAddress", "127.0.0.1") \
        .config("spark.sql.shuffle.partitions", "1") \
        .master("local[*]") \
        .getOrCreate()
    yield spark
    spark.stop()


def test_create_sample_dataframe(spark):
    """Test that create_sample_dataframe returns a DataFrame with correct data."""
    df = create_sample_dataframe(spark)

    # Check schema
    assert df.columns == ["Name", "Age"]

    # Check data
    rows = df.collect()
    assert len(rows) == 3

    # Check specific values
    names = [row["Name"] for row in rows]
    ages = [row["Age"] for row in rows]

    assert names == ["Alice", "Bob", "Charlie"]
    assert ages == [25, 30, 35]


def test_dataframe_schema(spark):
    """Test that the DataFrame has the correct schema."""
    df = create_sample_dataframe(spark)

    schema = df.schema
    assert len(schema.fields) == 2
    assert schema.fields[0].name == "Name"
    assert schema.fields[0].dataType.simpleString() == "string"
    assert schema.fields[1].name == "Age"
    assert schema.fields[1].dataType.simpleString() == "bigint"