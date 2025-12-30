# PySpark ETL Project

A production-ready PySpark ETL (Extract, Transform, Load) pipeline for processing employee data with comprehensive testing, CI/CD, and containerization support.

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
├── data/                        # Input data files
│   └── employees.csv           # Sample employee data
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

3. **Run the ETL pipeline:**
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
- Reads employee data from CSV files
- Automatic schema inference
- Error handling for missing files

### Transform Phase
- **Data Cleaning**: Removes records with missing values
- **Categorization**:
  - Salary categories: High (≥$80k), Medium (≥$60k), Low (<$60k)
  - Age groups: Young (<30), Middle (30-39), Senior (≥40)
- **Aggregation**: Calculates department average salaries
- **Filtering**: Keeps only employees above department average

### Load Phase
- Supports Parquet, CSV, and JSON output formats
- Automatic directory creation
- Overwrite mode for idempotent runs

### Sample Output

```
+-----------+-----+---+-------------+------+---------------+-------+---------------+
| Department| Name|Age|         City|Salary|Salary_Category|Age_Group|Dept_Avg_Salary|
+-----------+-----+---+-------------+------+---------------+-------+---------------+
|Engineering|  Bob| 30|San Francisco| 85000|           High|   Middle|        80000.0|
|      Sales|Frank| 40|       Denver| 90000|           High|   Senior|       74333.33|
|  Marketing|  Ivy| 29|     Portland| 72000|         Medium|    Young|        71000.0|
+-----------+-----+---+-------------+------+---------------+-------+---------------+
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