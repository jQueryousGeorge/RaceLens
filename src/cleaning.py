# Pure Python logic for data cleaning utils
import re
from typing import List, Dict, Any, Optional

"""
- This is an object-oriented approach to the cleaning methods used in the Jupyter Notebook `src/data_cleaning.ipynb`.
- `cleaning.py` does not support any of the data cleaning process for this repo. Instead, it serves as a template for applying a "vanilla" Python version of the `data_cleaning.ipynb` notebook via an OOP approach.
- To test this module and learn how to execute it, please see the very bottom of the file.

NOTE: This module provides pure Python utilities that work with dictionaries/lists. The main data pipeline 
now uses Parquet format for better performance and automatic dtype preservation. This module remains 
useful for environments where pandas is not available or when working with raw Python data structures.
"""

class DataCleaner:
	"""
	DataCleaner provides Python 'utility classmethods' for cleaning tabular data represented as lists of dictionaries.

	It includes methods for missing value detection, currency + distance normalization, string tidying,
	duplicate value detection, and batch cleaning of rows. No pandas dependency is required.
	
	The class is specifically tailored to handle data/columns that are found in the provided `dataset_test` 
	file (...named `dataset_test_csv.csv` in my repo and can be located in the `~/data/raw/` directory)
	
	IMPORTANT: The main data pipeline now uses Parquet format with pandas for optimal performance and 
	automatic dtype preservation. This pure Python class is provided for reference and environments 
	where pandas is not available.
	"""

	NA_TOKENS = {'NA','N/A','n/a','NULL','null','None','.','-','—',''}

	@classmethod
	def is_missing(cls, val: Any) -> bool:
		"""
		Return True if a data/cell value is considered missing (None, empty string, or in NA_TOKENS).
		
		- Args:
			val: Any value to check.
		- Returns:
			bool: True if missing, False otherwise.
		"""
		if val is None:
			return True
		if isinstance(val, str):
			return val.strip() in cls.NA_TOKENS or val.strip() == ''
		return False

	@classmethod
	def clean_distance(cls, val: Any) -> Optional[float]:
		"""
		Extract the numeric part from a distance string (e.g., '4.32F' -> 4.32, where 'F' = furlongs).
		Args:
			val: The value to clean (string or number).
		Returns:
			float or None: The numeric value, or None if missing/invalid.
		"""
		if cls.is_missing(val):
			return None
		match = re.search(r"([+-]?\d+(?:\.\d+)?)", str(val))
		return float(match.group(1)) if match else None

	@classmethod
	def clean_currency(cls, val: Any) -> Optional[float]:
		"""
		Remove $ and , from a currency string and return as float.
		Args:
			val: The value to clean (string or number).
		Returns:
			float or None: The numeric value, or None if missing/invalid.
		"""
		if cls.is_missing(val):
			return None
		
		# Handle if already numeric
		if isinstance(val, (int, float)):
			return float(val)
		
		s = re.sub(r"[\$,]", "", str(val)).strip()
		if not s:
			return None
		
		try:
			value = float(s)
			# Validate reasonable currency range
			if value < 0:
				print(f"Warning: Negative currency value: {value}")
			elif value > 1e9:  # $1 billion seems unreasonable for a race purse
				print(f"Warning: Extremely large currency value: {value}")
			return value
		except ValueError:
			print(f"Warning: Cannot parse currency value: {val}")
			return None

	@classmethod
	def tidy_string(cls, val: Any) -> Optional[str]:
		"""
		Convert empty or whitespace-only strings to None, else return the stripped string.
		Args:
			val: The value to tidy.
		Returns:
			str or None: Tidied string or None if missing.
		"""
		if cls.is_missing(val):
			return None
		return str(val).strip()

	@classmethod
	def clean_row(cls, row: Dict[str, Any]) -> Dict[str, Any]:
		"""
		Clean a single row of raw data (dictionary of column:value pairs).
		Renames columns, normalizes distance/currency, and tidies strings.
		Args:
			row: Dictionary representing a data row.
		Returns:
			dict: Cleaned row.
		"""
		out = dict(row)
		# Rename columns
		rename_map = {
			"Distance": "distance",
			"Purse": "purse",
			"Field_size": "field_size",
			"Earnings": "earnings",
			"Final Odds": "final_odds",
		}
		for old, new in rename_map.items():
			if old in out:
				out[new] = out.pop(old)

		# Clean distance
		if 'distance' in out:
			out['distance'] = cls.clean_distance(out['distance'])

		# Clean currency columns
		for money_col in ['purse', 'earnings']:
			if money_col in out:
				out[money_col] = cls.clean_currency(out[money_col])

		# Tidy all string columns (convert empty/whitespace to None)
		for k, v in out.items():
			if isinstance(v, str):
				out[k] = cls.tidy_string(v)

		return out

	@classmethod
	def clean_data(cls, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
		"""
		Clean a list of data rows (list of dictionaries).
		Args:
			rows: List of dictionaries representing data rows.
		Returns:
			list: List of cleaned rows.
		"""
		return [cls.clean_row(row) for row in rows]

	@classmethod
	def find_missing(cls, rows: List[Dict[str, Any]]) -> Dict[str, int]:
		"""
		Count missing values per column in a list of data rows.
		Args:
			rows: List of dictionaries representing data rows.
		Returns:
			dict: Mapping of column name to missing value count.
		"""
		if not rows:
			return {}
		cols = rows[0].keys()
		missing = {col: 0 for col in cols}
		for row in rows:
			for col in cols:
				if cls.is_missing(row.get(col)):
					missing[col] += 1
		return missing

	@classmethod
	def find_duplicates(cls, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
		"""
		Return duplicate rows (exact matches) from a list of data rows.
		Args:
			rows: List of dictionaries representing data rows.
		Returns:
			list: List of duplicate rows.
		"""
		seen = set()
		dups = []
		for row in rows:
			row_tuple = tuple(sorted(row.items()))
			if row_tuple in seen:
				dups.append(row)
			else:
				seen.add(row_tuple)
		return dups

if __name__ == "__main__":
    # Create test data:
    rows = [
        {
            "Distance": "4.32F",
            "Purse": "$4,500.00",
            "Earnings": "1000",
            "Field_size": "10",
            "Final Odds": "2.5",
            "SomeCol": "   ",
        },
        {
            "Distance": "5.0F",
            "Purse": "NA",
            "Earnings": "",
            "Field_size": "8",
            "Final Odds": "3.1",
            "SomeCol": "Horse",
        }
    ]

    cleaned = DataCleaner.clean_data(rows)

    print("Cleaned data:", cleaned)
    print("Missing counts:", DataCleaner.find_missing(cleaned))
    print("Duplicates:", DataCleaner.find_duplicates(cleaned))

"""
- How to use this file with the above test data??:

To test this file, just run " python3 src/cleaning.py " in your Terminal
    -- Note: the command `python3` above varies based on OS.
        --- If you're on Windows, just use "python src/cleaning.py" in PWSH.
		--- If you're on macOS or a Linux-based machine, you will use "python3 src/cleaning.py"
		
"""