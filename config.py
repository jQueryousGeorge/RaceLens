"""
Configuration file for RaceLens project.

This module defines all project paths as constants to avoid hardcoding throughout notebooks.
All paths are defined relative to the project root directory.

Usage:
    from src.config import DATA_RAW, DATA_PROCESSED
    
    # Load cleaned data
    df = pd.read_parquet(DATA_PROCESSED / 'cleaned_data.parquet')
"""

import sys
from pathlib import Path

# Check Python version (requires 3.12+)
if sys.version_info < (3, 12):
    raise RuntimeError(
        f"Python 3.12 or higher is required. "
        f"You are using Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}. "
        f"Please upgrade your Python version."
    )

# Project root directory (where config.py is located)
PROJECT_ROOT = Path(__file__).parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW = DATA_DIR / "raw"
DATA_PROCESSED = DATA_DIR / "processed"

# Raw data files
RAW_CSV = DATA_RAW / "dataset_test_csv.csv"
RAW_RACES_SHEET = DATA_RAW / "races_sheet.xlsx"
RAW_HORSES_PPS = DATA_RAW / "horses_pps.xlsx"

# Processed data files
CLEANED_DATA_PARQUET = DATA_PROCESSED / "cleaned_data.parquet"
VALIDATION_SUMMARY_JSON = DATA_PROCESSED / "data_validation_summary.json"

# Notebooks directories
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
NOTEBOOKS_EDA = NOTEBOOKS_DIR / "eda"
NOTEBOOKS_PAST_PERF = NOTEBOOKS_DIR / "past_performance"

# Reports directory
REPORTS_DIR = PROJECT_ROOT / "reports"

# Source code directory
SRC_DIR = PROJECT_ROOT / "src"

# Tests directory
TESTS_DIR = PROJECT_ROOT / "tests"


def ensure_directories():
    """
    Create all necessary directories if they don't exist.
    Useful for setting up a fresh clone of the repository.
    """
    directories = [
        DATA_DIR, DATA_RAW, DATA_PROCESSED,
        NOTEBOOKS_DIR, NOTEBOOKS_EDA, NOTEBOOKS_PAST_PERF,
        REPORTS_DIR, SRC_DIR, TESTS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    print("All project directories verified/created")


if __name__ == "__main__":
    # Print all configured paths for verification
    print("=" * 60)
    print("RaceLens Project Configuration")
    print("=" * 60)
    print(f"\nProject Root: {PROJECT_ROOT}")
    print(f"\nData Directories:")
    print(f"  Raw Data: {DATA_RAW}")
    print(f"  Processed Data: {DATA_PROCESSED}")
    print(f"\nKey Data Files:")
    print(f"  Raw CSV: {RAW_CSV}")
    print(f"  Cleaned Parquet: {CLEANED_DATA_PARQUET}")
    print(f"\nNotebook Directories:")
    print(f"  EDA: {NOTEBOOKS_EDA}")
    print(f"  Past Performance: {NOTEBOOKS_PAST_PERF}")
    print(f"\nReports: {REPORTS_DIR}")
    print("=" * 60)
    
    # Verify directories
    print("\nVerifying directory structure...")
    ensure_directories()

