import pytest
import os
import shutil
from pyspark.sql import SparkSession
from src.etl.etl import extract_data, transform_data, load_data
from src.utils.spark_utils import create_spark_session


@pytest.fixture(scope="session")
def spark():
    """Create a Spark session for testing."""
    spark_session = create_spark_session("ETL Test", {
        "spark.driver.bindAddress": "127.0.0.1",
        "spark.sql.shuffle.partitions": "1",
        "spark.master": "local[*]"
    })
    yield spark_session
    spark_session.stop()


@pytest.fixture
def sample_data_path(tmp_path):
    """Create a temporary CSV file with sample data."""
    csv_content = """Name,Age,City,Salary,Department
Alice,25,New York,75000,Engineering
Bob,30,San Francisco,85000,Engineering
Charlie,35,Chicago,65000,Sales
Diana,28,Boston,70000,Marketing"""

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
    assert df.columns == ["Name", "Age", "City", "Salary", "Department"]

    # Check data types
    assert df.schema.fields[0].name == "Name"
    assert df.schema.fields[1].name == "Age"
    assert df.schema.fields[1].dataType.simpleString() == "int"


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

    # Check new columns were added (Department becomes first after join)
    expected_columns = ["Department", "Name", "Age", "City", "Salary",
                       "Salary_Category", "Age_Group", "Dept_Avg_Salary"]
    assert transformed_df.columns == expected_columns

    # Check salary categories (at least one should exist)
    salary_categories = [row["Salary_Category"] for row in transformed_df.collect()]
    assert len(salary_categories) > 0
    assert all(cat in ["High", "Medium", "Low"] for cat in salary_categories)

    # Check age groups (at least one should exist)
    age_groups = [row["Age_Group"] for row in transformed_df.collect()]
    assert len(age_groups) > 0
    assert all(group in ["Young", "Middle", "Senior"] for group in age_groups)


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
    run_etl_pipeline(sample_data_path, output_path, {"spark.sql.shuffle.partitions": "1"})

    # Verify output exists
    assert os.path.exists(output_path)

    # Check that parquet files were created
    parquet_files = [f for f in os.listdir(output_path) if f.endswith('.parquet')]
    assert len(parquet_files) > 0

    # Note: We can't read back with Spark here because run_etl_pipeline stops the session
    # In a real scenario, you'd verify the output separately