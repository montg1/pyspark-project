import pytest
import os
from src.etl.etl import extract_data, transform_data, load_data
from src.utils.spark_utils import create_spark_session


@pytest.fixture(scope="session")
def spark():
    """Create a Spark session for testing."""
    spark_session = create_spark_session(
        "ETL Test",
        {
            "spark.driver.bindAddress": "127.0.0.1",
            "spark.sql.shuffle.partitions": "1",
            "spark.master": "local[*]",
        },
    )
    yield spark_session
    spark_session.stop()


@pytest.fixture
def sample_data_path(tmp_path):
    """Create a temporary CSV file with sample wine data."""
    csv_content = """,country,description,designation,points,price,province,region_1,region_2,taster_name,taster_twitter_handle,title,variety,winery
0,US,"A crisp, clean wine",Reserve,85,25.0,California,Napa Valley,,John Doe,@johndoe,Test Wine 2015,Chardonnay,Test Winery
1,US,"Rich and full-bodied",Grand Cru,92,45.0,California,Napa Valley,,Jane Doe,@janedoe,US Wine 2018,Cabernet Sauvignon,US Wines
2,France,"Light and fruity",Classico,88,30.0,Bordeaux,,,@janedoe,@janedoe,French Wine 2017,Sangiovese,French Wines
3,France,"Bold and spicy",Reserva,95,35.0,Bordeaux,,,Carlos Lopez,@carloslopez,Another French 2016,Tempranillo,French Wines"""

    csv_file = tmp_path / "test_data.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)


@pytest.fixture
def output_path(tmp_path):
    """Create a temporary output directory."""
    return str(tmp_path / "output")


def test_extract_data(spark, sample_data_path):
    """Test data extraction from CSV."""
    df = extract_data(spark, sample_data_path)

    assert df.count() == 4
    expected_columns = [
        "_c0",
        "country",
        "description",
        "designation",
        "points",
        "price",
        "province",
        "region_1",
        "region_2",
        "taster_name",
        "taster_twitter_handle",
        "title",
        "variety",
        "winery",
    ]
    assert df.columns == expected_columns

    # Check data types
    assert df.schema.fields[1].name == "country"
    assert df.schema.fields[4].name == "points"
    assert df.schema.fields[4].dataType.simpleString() == "int"
    assert df.schema.fields[5].name == "price"
    assert df.schema.fields[5].dataType.simpleString() == "double"


def test_extract_data_file_not_found(spark):
    """Test that extract_data raises error for missing file."""
    with pytest.raises(FileNotFoundError):
        extract_data(spark, "nonexistent_file.csv")


def test_transform_data(spark, sample_data_path):
    """Test data transformation."""
    # First extract
    df = extract_data(spark, sample_data_path)

    # Then transform
    transformed_df = transform_data(df)

    # Check new columns were added
    expected_columns = [
        "country",
        "_c0",
        "description",
        "designation",
        "points",
        "price",
        "province",
        "region_1",
        "region_2",
        "taster_name",
        "taster_twitter_handle",
        "title",
        "variety",
        "winery",
        "Quality_Category",
        "Price_Category",
        "Country_Avg_Points",
        "Country_Avg_Price",
        "Wine_Count",
    ]
    assert transformed_df.columns == expected_columns

    # Check quality categories
    quality_categories = [row["Quality_Category"] for row in transformed_df.collect()]
    assert len(quality_categories) > 0
    assert all(
        cat in ["Excellent", "Good", "Average", "Below Average"]
        for cat in quality_categories
    )

    # Check price categories
    price_categories = [row["Price_Category"] for row in transformed_df.collect()]
    assert len(price_categories) > 0
    assert all(cat in ["Premium", "Mid-Range", "Budget"] for cat in price_categories)


def test_load_data_parquet(spark, sample_data_path, output_path):
    """Test data loading to Parquet format."""
    # Extract and transform
    df = extract_data(spark, sample_data_path)
    transformed_df = transform_data(df)

    # Load
    load_data(transformed_df, output_path, "parquet")

    # Verify file was created
    assert os.path.exists(output_path)
    assert any(f.endswith(".parquet") for f in os.listdir(output_path))


def test_load_data_csv(spark, sample_data_path, output_path):
    """Test data loading to CSV format."""
    # Extract and transform
    df = extract_data(spark, sample_data_path)
    transformed_df = transform_data(df)

    # Load
    csv_output = output_path + "_csv"
    load_data(transformed_df, csv_output, "csv")

    # Verify file was created
    assert os.path.exists(csv_output)
    assert any(f.endswith(".csv") for f in os.listdir(csv_output))


def test_load_data_invalid_format(spark, sample_data_path, output_path):
    """Test that load_data raises error for invalid format."""
    df = extract_data(spark, sample_data_path)

    with pytest.raises(ValueError, match="Unsupported format"):
        load_data(df, output_path, "invalid_format")


def test_etl_pipeline_integration(sample_data_path, output_path):
    """Integration test for the complete ETL pipeline."""
    from src.etl.etl import run_etl_pipeline

    # Run ETL (this will create its own Spark session and stop it)
    run_etl_pipeline(
        sample_data_path, output_path, {"spark.sql.shuffle.partitions": "1"}
    )

    # Verify output exists
    assert os.path.exists(output_path)

    # Check that parquet files were created
    parquet_files = [f for f in os.listdir(output_path) if f.endswith(".parquet")]
    assert len(parquet_files) > 0

    # Note: We can't read back with Spark here because run_etl_pipeline stops the session
    # In a real scenario, you'd verify the output separately
