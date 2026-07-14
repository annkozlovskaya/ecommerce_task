"""
ETL pipeline package.

Contains the complete Extract-Transform-Load workflow
for generating the sales performance report.
"""

from .pipeline import Pipeline

__all__ = [
    "Pipeline",
]