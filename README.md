# PySpark ETL Project

A production-ready PySpark ETL (Extract, Transform, Load) pipeline for processing wine reviews data with comprehensive testing, CI/CD, and containerization support.

## 🏗️ Project Structure

```
pyspark-etl-project/
├── src/                          # Source code
│   ├── etl/                     # ETL pipeline modules
│   │   ├── __init__.py
│   │   └── etl.py              # Main ETL logic
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   └── spark_utils.py      # Spark utilities
│   ├── config/                  # Configuration
│   │   ├── __init__.py
│   │   └── settings.py         # App settings
│   ├── tests/                   # Unit tests
│   │   ├── __init__.py
│   │   ├── test_etl.py         # ETL tests
│   │   └── test_main.py        # Main tests
│   └── main.py                 # Application entry point
├── scripts/                     # Executable scripts
│   └── read_output.py          # Data reader script
├── data/                        # Input data files (not included in repo)
│   ├── winemag-data-130k-v2.csv # Wine reviews dataset (download from Kaggle)
│   ├── wine_reviews_sample.csv  # Sample wine data for testing
│   └── employees.csv            # Legacy employee data
├── config/                      # Configuration files
├── docs/                        # Documentation
├── output/                      # Generated output (gitignored)
├── .github/workflows/           # CI/CD pipelines
│   └── test.yml                # GitHub Actions workflow
├── Dockerfile                   # Container definition
├── docker-compose.yml          # Container orchestration
├── setup.py                     # Package configuration
├── Makefile                     # Development automation
├── requirements.txt             # Dependencies
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Java 11
- Make (optional, for using Makefile)

### Local Development

1. **Clone and setup:**
   ```bash
   git clone https://github.com/montg1/pyspark-project.git
   cd pyspark-project
   ```

2. **Install dependencies:**
   ```bash
   # Using pip
   export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"
   pip install -e .

   # Or using Make
   make install
   ```

3. **Download wine reviews data:**
   ```bash
   # Option 1: Using Kaggle CLI (recommended)
   pip install kaggle
   kaggle datasets download -d zynicide/wine-reviews -p data/
   cd data && unzip wine-reviews.zip

   # Option 2: Manual download
   # Go to https://www.kaggle.com/datasets/zynicide/wine-reviews
   # Download the dataset and place winemag-data-130k-v2.csv in the data/ directory

   # Option 3: Use sample data for testing
   # The pipeline will work with the included wine_reviews_sample.csv
   ```

4. **Run the ETL pipeline:**
   ```bash
   # Using Python module
   python -m src.main

   # Or using Make
   make run
   ```

4. **View results:**
   ```bash
   # Using script
   python scripts/read_output.py

   # Or using Make
   make read-output
   ```

## 🧪 Testing

### Run Tests Locally

```bash
# Using pytest directly
export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"
python -m pytest src/tests/ -v

# Or using Make
make test

# With coverage
make test-cov
```

### CI/CD

This project uses GitHub Actions for automated testing:

- **Triggers**: Push to `main` branch and pull requests
- **Tests**: Unit tests, linting, and ETL pipeline execution
- **Environment**: Ubuntu with Python 3.9 and Java 11

## 🐳 Containerization

### Using Docker

```bash
# Build image
docker build -t pyspark-etl .

# Run container
docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output pyspark-etl
```

### Using Docker Compose

```bash
# Run ETL pipeline
docker-compose up pyspark-etl

# Development environment
docker-compose up pyspark-etl-dev

# Run tests in container
docker-compose up test
```

## 📊 ETL Pipeline Details

### Extract Phase
- Reads wine reviews data from CSV files
- Automatic schema inference
- Error handling for missing files

### Transform Phase
- **Data Cleaning**: Removes records with missing critical values (country, points, price, variety)
- **Categorization**:
  - Quality categories: Excellent (≥95 pts), Good (≥85 pts), Average (≥75 pts), Below Average (<75 pts)
  - Price categories: Premium (≥$100), Mid-Range (≥$50), Budget (<$50)
- **Aggregation**: Calculates country-level statistics (average points, average price, wine count)
- **Filtering**: Keeps only wines above their country's average points rating

### Load Phase
- Supports Parquet, CSV, and JSON output formats
- Automatic directory creation
- Overwrite mode for idempotent runs

### Sample Output

```
+---------+---+--------------------+--------------------+------+-----+---------------+--------+--------+-----------------+---------------------+--------------------+----------+-------------+----------------+--------------+------------------+-----------------+----------+
|  country|_c0|         description|         designation|points|price|        province|region_1|region_2|      taster_name|taster_twitter_handle|               title|   variety|       winery|Quality_Category|Price_Category|Country_Avg_Points|Country_Avg_Price|Wine_Count|
+---------+---+--------------------+--------------------+------+-----+---------------+--------+--------+-----------------+---------------------+--------------------+----------+-------------+----------------+--------------+------------------+-----------------+----------+
|Argentina| 16|Baked plum, molas...|               Felix|    87| 30.0|           Other|Cafayate|    NULL|Michael Schachner|          @wineschach|Felix Lavaque 201...|    Malbec|Felix Lavaque|            Good|        Budget|             86.71|            24.51|      3756|
|    Chile|103|A bright nose wit...|Single Vineyard F...|    87| 18.0|    Leyda Valle|    NULL|    NULL|Michael Schachner|          @wineschach|Leyda 2015 Single...|Chardonnay|        Leyda|            Good|        Budget|              86.5|            20.79|      4415|
+---------+---+--------------------+--------------------+------+-----+---------------+--------+--------+-----------------+---------------------+--------------------+----------+-------------+----------------+--------------+------------------+-----------------+----------+
```

## 🛠️ Development

### Code Quality

```bash
# Linting
make lint

# Code formatting
make format

# Full CI simulation
make ci
```

### Project Commands

```bash
# Install for development
make install-dev

# Setup pre-commit hooks
make setup-dev

# Clean up
make clean

# Generate documentation
make docs
```

## 📋 Configuration

Key configuration files:

- **`src/config/settings.py`**: Application settings and thresholds
- **`requirements.txt`**: Python dependencies
- **`setup.py`**: Package configuration
- **`Makefile`**: Development automation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with PySpark for scalable data processing
- Uses pytest for comprehensive testing
- Containerized with Docker for portability
- CI/CD powered by GitHub Actions