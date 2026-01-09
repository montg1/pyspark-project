"""
FastAPI application for wine reviews data exploration.
Exposes endpoints for accessing and querying transformed ETL data.
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from src.api.data_reader import DataReader

# Initialize FastAPI app
app = FastAPI(
    title="Wine Reviews API",
    description=(
        "API for exploring wine reviews data "
        "processed by PySpark ETL pipeline"
    ),
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data reader (lazy load on first API call)
_data_reader = None


def get_data_reader() -> DataReader:
    """Get or initialize DataReader instance."""
    global _data_reader  # noqa: F824
    if _data_reader is None:
        _data_reader = DataReader()
    return _data_reader


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Dict with status
    """
    return {"status": "healthy"}


@app.get("/stats/countries")
async def get_country_statistics() -> List[Dict[str, Any]]:
    """
    Get statistics grouped by country.

    Returns:
        List of countries with average points, price, and wine count
    """
    reader = get_data_reader()
    return reader.get_country_stats()


@app.get("/stats/quality-distribution")
async def get_quality_distribution() -> Dict[str, int]:
    """
    Get distribution of wines by quality category.

    Returns:
        Dict mapping quality categories to counts
    """
    reader = get_data_reader()
    return reader.get_quality_distribution()


@app.get("/stats/price-distribution")
async def get_price_distribution() -> Dict[str, int]:
    """
    Get distribution of wines by price category.

    Returns:
        Dict mapping price categories to counts
    """
    reader = get_data_reader()
    return reader.get_price_distribution()


@app.get("/stats/top-varieties")
async def get_top_varieties(
    limit: int = Query(10, ge=1, le=50)
) -> List[Dict[str, Any]]:
    """
    Get top wine varieties by count.

    Args:
        limit: Number of top varieties to return (1-50)

    Returns:
        List of varieties with their counts
    """
    reader = get_data_reader()
    return reader.get_top_varieties(limit=limit)


@app.get("/stats/total-count")
async def get_total_count() -> Dict[str, int]:
    """
    Get total count of wines in the dataset.

    Returns:
        Dict with total count
    """
    reader = get_data_reader()
    count = reader.get_total_count()
    return {"total_wines": count}


@app.get("/wines")
async def get_wines(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
) -> Dict[str, Any]:
    """
    Get paginated wine reviews data.

    Args:
        limit: Number of records to return (1-500)
        offset: Number of records to skip

    Returns:
        Dict with wines list and pagination info
    """
    reader = get_data_reader()
    wines = reader.get_wine_data(limit=limit, offset=offset)
    total = reader.get_total_count()

    return {
        "data": wines,
        "limit": limit,
        "offset": offset,
        "total": total
    }


@app.on_event("shutdown")
def shutdown_event():
    """Clean up Spark session on shutdown."""
    global _data_reader  # noqa: F824
    if _data_reader:
        _data_reader.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
