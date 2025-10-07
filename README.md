# RaceLens

RaceLens is a complete data science project focused on analyzing and predicting horse racing outcomes using machine learning techniques. The project shows an end-to-end data science workflow from data cleaning through advanced modeling.

## Requirements

**Python 3.12 is required** for this project due to compatibility requirements with the latest data science libraries.

## Project Overview

This project analyzes horse racing entries to build predictive models for race outcomes. Key achievements include:
- Strong data cleaning pipeline handling 30+ columns
- Advanced DNF (Did Not Finish) race handling to prevent data skew
- Complete exploratory data analysis revealing industry insights
- Machine learning models achieving 60.6% AUC (better than random)
- Production-ready code with full documentation

## Project Structure

```
RaceLens/
├── README.md
├── requirements.txt
├── pyproject.toml                 # Python dependency management
├── data/
│   ├── processed/
│   │   └── cleaned_data.parquet   # Cleaned data in efficient Parquet format
│   └── raw/
│       ├── dataset_test_csv.csv   # Main dataset
│       ├── races_sheet.xlsx       # Race-level data
│       └── horses_pps.xlsx        # Horse performance data
├── notebooks/
│   ├── 01_data_exploration.ipynb # Initial data exploration
│   ├── eda/
│   │   └── 01_races_eda.ipynb    # Complete EDA
│   ├── past_performance/
│   │   ├── logistic_analysis_1.ipynb    # Basic logistic regression
│   │   ├── logistic_analysis_2.ipynb    # Alternative features model
│   │   └── xgboost_logistic_analysis_3.ipynb  # Advanced XGBoost model
│   |
├── reports/
│   └── final_report.md            # Executive summary and findings
├── src/
│   ├── __init__.py
│   ├── config.py                  # Project configuration and path constants
│   ├── cleaning.py                # OOP reference implementation (not used)
│   └── data_cleaning.ipynb        # Main data cleaning pipeline
└── tests/
    └── test_performance.py        # Performance testing utilities
```

## Key Components

### 1. Data Cleaning Pipeline (data_cleaning.ipynb)
The main data cleaning notebook that:
- Handles missing values with custom NA tokens
- Cleans currency fields (removes $, commas)
- Parses distance values (e.g., "4.32F" → 4.32)
- **Identifies DNF races (speed_figure = 999) for special handling**
- Optimizes memory usage with categorical dtypes
- Exports to Parquet format preserving all dtypes

### 2. Critical Data Quality: DNF (Did Not Finish) Handling
An approach to handle DNF races that could severely skew results:
- **Problem**: Speed figure of 999 indicates DNF races (horses that didn't finish the race)
- **Impact**: Including these in averages would artificially inflate speed metrics
- **Solution**: 
  - DNF races are identified and excluded from speed calculations
  - DNF rate is tracked as a predictive feature (reliability indicator)
  - Horses with all DNF races are excluded from analysis
- **Result**: More accurate speed metrics and improved model performance

### 3. Exploratory Data Analysis (`01_data_exploration.ipynb`, `01_races_eda.ipynb`)
Complete analysis revealing:
- Industry structure and concentration
- Stakes racing premium (5.2x higher purses)
- Foreign vs domestic horse distribution
- Seasonal patterns and track specialization
- Field size dynamics and competition intensity
- DNF race prevalence and impact

### 4. Predictive Modeling
Three progressive modeling approaches:

#### a. Basic Logistic Regression (`logistic_analysis_1.ipynb`)
- Features: win rate, average speed figure (DNF-corrected), DNF rate
- Performance: ~57% AUC
- Key finding: Past win rate is significant predictor

#### b. Alternative Features Model (`logistic_analysis_2.ipynb`)
- Features: win percentage, final odds
- Performance: Similar ~57% AUC
- Insight: Final odds provide alternative to speed figures

#### c. XGBoost with Feature Engineering (`xgboost_logistic_analysis_3.ipynb`)
- 14 engineered features including consistency metrics
- Performance: 60.6% AUC
- Key features: win rate, speed consistency, jockey/trainer consistency

### 5. Configuration Module (`config.py`)
Centralized configuration file defining all project paths as constants to avoid hardcoding throughout notebooks. Provides standardized path management for data files, notebooks, and reports.

### 6. Reference Implementation (`cleaning.py`)
A demonstration of OOP-based data cleaning approach showing modular, reusable design patterns. This file is NOT used in the actual pipeline but serves as a reference for production-style code.

## Getting Started

### Prerequisites
- **Python 3.12+** (Required)
- pip (Python package manager)
- virtualenv or venv

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/jQueryousGeorge/RaceLens.git
    cd RaceLens
    ```

2. **Verify Python Version:**
    ```bash
    python --version  # Should be 3.12.x (not 3.13+)
    ```
    
    If you need to install Python 3.12:
    
    **Ubuntu/Debian:**
    ```bash
    sudo apt-get update
    sudo apt-get install -y python3.12 python3.12-dev python3.12-venv
    ```
    
    **macOS (with Homebrew):**
    ```bash
    brew install python@3.12
    ```
    
    **Windows:**
    Download Python 3.12 from [python.org](https://www.python.org/downloads/)

3. **Create a Virtual Environment:**
    
    **macOS & Linux:**
    ```bash
    python3.12 -m venv venv
    source venv/bin/activate
    ```
    
    **Windows (PowerShell):**
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

4. **Install dependencies:**
    
    **Option A: Using pyproject.toml (Recommended)**
    ```bash
    # Upgrade pip first
    python -m pip install --upgrade pip setuptools wheel
    
    # Install in editable mode with automatic version checking
    pip install -e .
    ```
    
    **Option B: Using requirements.txt (Traditional)**
    ```bash
    # Upgrade pip first
    python -m pip install --upgrade pip setuptools wheel
    
    # Install dependencies
    pip install -r requirements.txt
    ```

5. **Run the data pipeline:**
    - Open `data_cleaning.ipynb` in Jupyter or VS Code
    - Execute all cells to clean the raw data
    - Continue with `01_data_exploration.ipynb` for initial analysis
    - Proceed to the `past_performance/` dir for modeling

### Troubleshooting

**ImportError or ModuleNotFoundError:**
- Ensure you're using Python 3.12+ (`python --version`)
- Make sure your virtual environment is activated
- Try reinstalling dependencies: `pip install --upgrade -r requirements.txt`

**Installation fails on Ubuntu/Debian:**
```bash
# Install required system libraries
sudo apt-get install -y libffi-dev python3.12-dev build-essential
```

**Jupyter notebook kernel issues:**
```bash
# Install ipykernel in your virtual environment
pip install ipykernel
python -m ipykernel install --user --name=venv
```

## Technical Highlights

- **Memory Efficiency**: Parquet format reduces file size by 68%
- **Type Safety**: All data types preserved through pipeline
- **DNF Handling**: Advanced approach to prevent speed figure inflation
- **Feature Engineering**: 14 engineered features for improved predictions
- **Centralized Configuration**: `config.py` provides standardized path management
- **Scalability**: Modular design allows easy extension
- **Documentation**: Complete inline documentation and analysis reports

## Results Summary

- Dataset: 60,752 race entries
- Horses analyzed: 15,143 with exactly 4 races
- Baseline win rate: 14.3% (2,168 winners)
- DNF races identified: ~6% of dataset
- Best model performance: 60.6% AUC (XGBoost)
- Key insight: Past performance provides modest but meaningful predictive power
- Business value: Models can provide slight edge for ranking horses

## Model Performance Comparison

| Model | AUC | Features | Key Finding |
|-------|-----|----------|-------------|
| Logistic Regression v1 | 0.569 | 3 (win rate, speed, DNF rate) | Win rate is strongest predictor |
| Logistic Regression v2 | 0.571 | 2 (win %, final odds) | Final odds alternative to speed |
| XGBoost (2 features) | 0.557 | 2 (same as LR v1) | Minimal improvement |
| XGBoost (14 features) | 0.606 | 14 engineered features | Best performance with feature engineering |

## Future Enhancements

- Incorporate additional data sources (weather, track conditions, jockey form)
- Deep learning approaches for sequence modeling
- Real-time prediction pipeline for live betting
- Interactive dashboards for race analysis
- Ensemble methods combining multiple model types

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with Python, pandas, scikit-learn, XGBoost, and Jupyter Notebooks
- Inspired by best practices in data science and reproducible research
- Special attention to data quality issues common in real-world datasets