# PySpark Project

This is a PySpark project.

## Setup

1. Install Java 11 (required for PySpark):
   ```bash
   brew install openjdk@11
   export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the main script:
   ```bash
   python main.py
   ```

## Testing

Run tests locally with:
```bash
export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH" && python -m pytest
```

## CI/CD

This project uses GitHub Actions for continuous integration. Tests run automatically on:
- Push to `main` branch
- Pull requests to `main` branch

The workflow includes:
- Python 3.9 setup
- Java 11 installation
- Dependency installation
- Automated test execution

- Python 3.8+
- Java 11
- PySpark 3.5.0