"""
Transformation package.

Contains business logic for filtering, enriching,
and aggregating event data into the final report.
"""

from .transformer import DataTransformer

__all__ = [
    "DataTransformer",
]