"""
Performance tests for the DataCleaner reference implementation.

NOTE: These tests validate the OOP-based reference implementation in src/cleaning.py.
The actual data cleaning pipeline uses src/data_cleaning.ipynb with pandas and Parquet format.
The DataCleaner class serves as a template for production-style code and environments
where pandas is not available.

For testing the actual data pipeline, refer to the validation checks within 
src/data_cleaning.ipynb (Cell 22) which includes:
- Data validation checks
- Outlier detection
- Cross-column validation
- Dtype verification
"""

import pytest
import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

from cleaning import DataCleaner


class TestPerformance:
    """Performance tests to ensure DataCleaner reference implementation is efficient"""
    
    def test_large_dataset_cleaning(self):
        """Test cleaning performance on larger dataset"""
        # Generate 1000 rows of test data
        large_dataset = []
        for i in range(1000):
            large_dataset.append({
                "Distance": f"{4 + i/1000}F",
                "Purse": f"${1000 + i},000.00",
                "Earnings": f"${100 + i}.00",
                "Field_size": str(5 + (i % 10)),
                "Final Odds": str(1.5 + i/100),
                "horse_name": f"Horse {i}",
                "track_id": f"TRK{i % 10}",
                "equipment": "B" if i % 2 else "     "
            })
        
        start_time = time.time()
        cleaned_data = DataCleaner.clean_data(large_dataset)
        elapsed_time = time.time() - start_time
        
        # Should complete in reasonable time (< 1 second for 1000 rows)
        assert elapsed_time < 1.0
        assert len(cleaned_data) == 1000
        
        # Spot check some values
        assert cleaned_data[0]["distance"] == 4.0
        assert cleaned_data[999]["distance"] == 4.999
    
    def test_find_duplicates_performance(self):
        """Test duplicate finding performance"""
        # Create dataset with some duplicates
        rows = []
        for i in range(500):
            rows.append({"id": i, "name": f"Horse {i}"})
        # Add 100 duplicates
        for i in range(100):
            rows.append({"id": i, "name": f"Horse {i}"})
        
        start_time = time.time()
        duplicates = DataCleaner.find_duplicates(rows)
        elapsed_time = time.time() - start_time
        
        assert elapsed_time < 0.5  # Should be very fast
        assert len(duplicates) == 100