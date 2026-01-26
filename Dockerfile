# Dockerfile for PySpark ETL Project

FROM python:3.9-slim

# Install Java (required for PySpark)
RUN apt-get update && \
    apt-get install -y default-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="$JAVA_HOME/bin:$PATH"
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY data/ ./data/

# Create output directory
RUN mkdir -p output

# Default command
CMD ["python", "-m", "src.main"]