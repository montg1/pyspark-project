"""
Utility for reading and querying transformed Parquet data from ETL output.
"""

import os
from typing import List, Dict, Any
from src.utils.spark_utils import create_spark_session


class DataReader:
    """Handle reading and querying transformed wine reviews data."""

    def __init__(self, data_path: str = "output/transformed_wine_reviews"):
        """
        Initialize DataReader with path to transformed data.

        Args:
            data_path (str): Path to Parquet directory from ETL pipeline
        """
        self.data_path = data_path
        self.spark = None
        self.df = None

    def load_data(self):
        """
        Load transformed data from Parquet files.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(self.data_path):
                print(f"⚠️  Data path not found: {self.data_path}")
                return False

            if self.spark is None:
                self.spark = create_spark_session("Data Reader API")

            self.df = self.spark.read.parquet(self.data_path)
            return True
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return False

    def get_country_stats(self) -> List[Dict[str, Any]]:
        """
        Get statistics by country.

        Returns:
            List[Dict]: Country statistics including average points,
                price, and wine count
        """
        if self.df is None:
            if not self.load_data():
                return []

        try:
            stats = self.df.groupBy("country").agg(
                {"points": "avg", "price": "avg", "variety": "count"}
            ).collect()

            result = []
            for row in stats:
                result.append({
                    "country": row[0],
                    "avg_points": (round(float(row[1]), 2)
                                   if row[1] else None),
                    "avg_price": (round(float(row[2]), 2)
                                  if row[2] else None),
                    "wine_count": int(row[3]) if row[3] else 0
                })
            return sorted(result, key=lambda x: x["wine_count"], reverse=True)
        except Exception as e:
            print(f"❌ Error getting country stats: {str(e)}")
            return []

    def get_quality_distribution(self) -> Dict[str, int]:
        """
        Get distribution of wines by quality category.

        Returns:
            Dict[str, int]: Count of wines in each quality category
        """
        if self.df is None:
            if not self.load_data():
                return {}

        try:
            dist = self.df.groupBy("Quality_Category").count().collect()
            result = {}
            for row in dist:
                result[row[0]] = int(row[1])
            return result
        except Exception as e:
            print(f"❌ Error getting quality distribution: {str(e)}")
            return {}

    def get_price_distribution(self) -> Dict[str, int]:
        """
        Get distribution of wines by price category.

        Returns:
            Dict[str, int]: Count of wines in each price category
        """
        if self.df is None:
            if not self.load_data():
                return {}

        try:
            dist = self.df.groupBy("Price_Category").count().collect()
            result = {}
            for row in dist:
                result[row[0]] = int(row[1])
            return result
        except Exception as e:
            print(f"❌ Error getting price distribution: {str(e)}")
            return {}

    def get_wine_data(
        self, limit: int = 100, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get paginated wine review data.

        Args:
            limit (int): Number of records to return
            offset (int): Number of records to skip

        Returns:
            List[Dict]: Wine review data
        """
        if self.df is None:
            if not self.load_data():
                return []

        try:
            limited_df = self.df.limit(offset + limit).collect()[offset:]
            result = []
            for row in limited_df:
                result.append(row.asDict())
            return result
        except Exception as e:
            print(f"❌ Error getting wine data: {str(e)}")
            return []

    def get_top_varieties(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top wine varieties by count.

        Args:
            limit (int): Number of varieties to return

        Returns:
            List[Dict]: Top varieties with counts
        """
        if self.df is None:
            if not self.load_data():
                return []

        try:
            top = (self.df.groupBy("variety").count()
                   .orderBy("count", ascending=False)
                   .limit(limit).collect())
            result = []
            for row in top:
                result.append({
                    "variety": row[0],
                    "count": int(row[1])
                })
            return result
        except Exception as e:
            print(f"❌ Error getting top varieties: {str(e)}")
            return []

    def get_total_count(self) -> int:
        """
        Get total count of wines in dataset.

        Returns:
            int: Total wine count
        """
        if self.df is None:
            if not self.load_data():
                return 0

        try:
            return int(self.df.count())
        except Exception as e:
            print(f"❌ Error getting total count: {str(e)}")
            return 0

    def close(self):
        """Close Spark session."""
        if self.spark:
            self.spark.stop()
