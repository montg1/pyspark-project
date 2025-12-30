"""
Main entry point for PySpark ETL project.
"""

from src.etl.etl import run_etl_pipeline


def main():
    """Main function to run the ETL pipeline."""
    print("🚀 Starting PySpark ETL Project")

    # Run the ETL pipeline with default configuration
    run_etl_pipeline()


if __name__ == "__main__":
    main()
