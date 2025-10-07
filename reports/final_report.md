# RaceLens: Horse Racing Prediction Analysis
## Executive Summary & Key Findings

### Project Overview
RaceLens is a data science project for predicting horse racing outcomes using historical performance data. This report synthesizes findings from multiple analytical approaches, including exploratory data analysis, logistic regression modeling, and advanced machine learning techniques using XGBoost.

### Data Foundation
- **Dataset Size**: 60,752 race entries
- **Horses Analyzed**: 15,143 horses with exactly 4 races each
- **Target Variable**: Binary classification - predicting win (1st place) vs. non-win in 4th race
- **Win Rate**: 14.3% baseline (2,168 winners out of 15,143 horses)
- **Critical Data Quality**: Identified and properly handled DNF (Did Not Finish) races

### Key Technical Achievements

#### 1. Data Pipeline Excellence
- Built strong data cleaning pipeline in Jupyter notebook format for transparency
- Implemented efficient Parquet format storage, reducing file size by 68%
- Created a reference OOP implementation demonstrating production-ready patterns
- **Critical DNF handling**: Identified races with speed_figure = 999 as DNF races
- Handled complex data challenges including:
  - Currency formatting ($4,500.00 → 4500.00)
  - Distance parsing (4.32F → 4.32 furlongs)
  - Missing value detection with custom NA tokens
  - Category optimization for memory efficiency
  - **DNF race exclusion from speed calculations**

#### 2. Critical Data Quality: DNF Race Handling
**Problem Identified**: 
- Speed figure values of 999 indicate DNF (Did Not Finish) races
- Including these in average calculations would severely inflate speed metrics
- Approximately 0.5% of races in dataset are DNF races

**Solution Implemented**:
- DNF races identified and excluded from all speed figure calculations
- DNF rate tracked as a predictive feature (horse reliability indicator)
- Horses with all 3 past races as DNF excluded from analysis
- Proper handling prevents artificially inflated averages

**Impact**:
- More accurate speed figure averages (preventing 10x inflation)
- Better model performance through clean data
- DNF rate itself becomes a predictive feature

#### 3. Statistical Modeling Progression

**Model 1: Basic Logistic Regression (DNF-Corrected)**
- Features: `win_rate_past_3`, `avg_speed_figure_past_3` (DNF-excluded), `dnf_rate_past_3`
- AUC: 0.569 (6.9% above random chance)
- Key Finding: Only win_rate was statistically significant (p<0.001)
- Pseudo R²: 0.003 (explains <1% of variance)

**Model 2: Final Odds Logistic Regression**
- Features: win_percentage_past_3, avg_final_odds_past_3
- AUC: 0.571 (slightly improved)
- Key Finding: Both features potentially significant
- Insight: Betting market odds contain predictive information

**Model 3: XGBoost with Feature Engineering**
- Features: 14 engineered features including:
  - Performance consistency metrics (speed_figure_std)
  - Recent form indicators (recent_speed_figure, speed_trend)
  - Competition level (avg_purse, avg_field_size)
  - Stability factors (jockey/trainer/distance consistency)
  - **DNF rate as reliability indicator**
- AUC: 0.606 (20.6% above random chance)
- Top predictors: `avg_position`, `recent_speed_figure`, `avg_speed_figure`

### Critical Business Insights

#### 1. Data Quality Impact
- **DNF Handling**: Proper exclusion of DNF races prevents major analytical errors
- **Without DNF handling**: Average speeds would be inflated
- **With DNF handling**: Accurate performance metrics enable valid predictions
- **Business Value**: Clean data is essential for any betting or selection system

#### 2. Predictive Factors Hierarchy
1. **Past Win Rate** (Most Important)
   - 80% increase in win odds for each additional past win
   - Consistent across all models
   - Clear signal: winners tend to keep winning

2. **Average Finishing Position**
   - Strong predictor in XGBoost model
   - Captures competitive consistency beyond just wins

3. **Recent Performance** (DNF-Corrected)
   - Recent speed figures more predictive than averages
   - Momentum matters in horse racing
   - DNF exclusion critical for accuracy

4. **Horse Reliability**
   - DNF rate indicates horse reliability
   - Horses with high DNF rates are poor bets
   - New feature enabled by proper data handling

#### 3. Model Performance Reality Check
- Best model AUC: 0.606
- This represents MODERATE predictive power
- Context: Professional handicappers achieve ~0.65-0.70 AUC
- Conclusion: Our models provide slight edge but aren't game-changing

#### 4. Why Predictions Are Limited
1. **Inherent Randomness**: Horse racing involves numerous uncontrolled variables
2. **Missing Critical Data**: 
   - Track conditions
   - Weather
   - Horse health/fitness
   - Jockey/trainer current form
   - Pre-race betting movements
3. **Sample Size**: Only 3 races to predict 4th limits pattern detection
4. **Class Changes**: Horses moving up/down in competition level

### Technical Methodology Strengths

1. **Proper ML Practices**
   - Train/test split (80/20) with stratification
   - No data leakage (strict temporal ordering maintained)
   - Consistent random state (42) for reproducibility
   - Multiple modeling approaches for comparison
   - **Proper handling of edge cases (DNF races)**

2. **Feature Engineering Excellence**
   - Created 14 meaningful features from raw data
   - Captured trend, consistency, and level metrics
   - **Added DNF rate as reliability indicator**
   - Avoided overfitting through careful selection

3. **Statistical Rigor**
   - Proper p-value interpretation
   - Odds ratio calculations for business understanding
   - Model comparison with consistent metrics
   - **Data quality validation before modeling**

### Data Quality Lessons Learned

1. **Critical Finding**: Speed figure of 999 indicates DNF races
2. **Impact**: ~0.5% of dataset required special handling
3. **Solution**: Systematic identification and exclusion from averages
4. **Result**: Clean, accurate metrics for modeling
5. **Business Insight**: Data quality issues can severely impact predictions if not addressed

### Practical Applications & Recommendations

#### Immediate Applications
1. **Horse Ranking System**
   - Use model probabilities to rank horses in upcoming races
   - Focus on races with clear probability separations
   - **Filter out horses with high DNF rates**
   - Combine with other factors for final decisions

2. **Training Insights**
   - Prioritize consistency in jockey/trainer combinations
   - Focus on maintaining competitive positioning
   - Track recent performance trends closely
   - **Monitor DNF rates as health/fitness indicator**

3. **Data Collection Priorities**
   - Implement collection of track conditions
   - Add weather data integration
   - Include workout times between races
   - Capture class/competition level changes
   - **Track reasons for DNF outcomes**

#### Next Steps for Model Enhancement
1. **Ensemble Approach**
   - Combine XGBoost with neural networks
   - Add LightGBM for alternative tree structure
   - Weight models based on race types

2. **Advanced Features**
   - Jockey/trainer historical win rates
   - Head-to-head past performance
   - Pace analysis (early/late speed)
   - Post position statistics
   - **DNF prediction as separate model**

3. **Specialized Models**
   - Separate models for sprint vs. route races
   - Track-specific models
   - Class-level predictions
   - **DNF likelihood prediction model**

### Value Proposition for Stakeholders

#### For Data Science Teams
- Shows complete ML pipeline from raw data to insights
- Shows progression from simple to complex models
- **Highlights critical importance of data quality checks**
- Provides reusable code architecture

#### For Business Analysts
- Measurable improvement: 21% better than random selection
- Identifies actionable factors for horse selection
- Quantifies impact of various performance metrics
- **Shows how data quality affects business outcomes**

#### For Racing Professionals
- Confirms importance of recent form
- Quantifies win consistency value
- **Reveals DNF rate as reliability indicator**
- Offers systematic approach to selection

### Conclusion

RaceLens successfully shows that historical performance data contains predictive signal for horse racing outcomes, achieving a 21% improvement over random chance through advanced feature engineering and machine learning techniques. **Critically, the project highlights the importance of thorough data quality analysis, as the identification and proper handling of DNF races prevented severe analytical errors that would have invalidated all results.**

While the predictive power remains moderate (AUC 0.606), the project establishes a solid foundation for:

1. **Systematic horse evaluation** with clean, accurate data
2. **Identification of key performance factors** including reliability metrics
3. **A scalable framework** with proper data quality controls
4. **Clear next steps** for achieving professional-grade predictions

The honest assessment of limitations, combined with strong technical implementation and careful attention to data quality, positions this project as a valuable proof-of-concept for data-driven decision making in horse racing. The modular architecture and complete documentation ensure easy extension and maintenance for future enhancements.

### Project Deliverables

1. **Clean, Analysis-Ready Data**: [cleaned_data.parquet](../data/processed/cleaned_data.parquet)
2. **Data Quality Documentation**: [data_validation_summary.json](../data/processed/data_validation_summary.json)
3. **Reusable Code Components**: 
   - [Data Cleaning Pipeline](../src/data_cleaning.ipynb)
   - [Configuration Module](../src/config.py)
   - [Reference OOP Implementation](../src/cleaning.py)
4. **Interactive Analysis Notebooks**: 
   - [Initial Exploration](../notebooks/01_data_exploration.ipynb)
   - [EDA](../notebooks/eda/01_races_eda.ipynb)
   - [Logistic Regression (DNF-Corrected)](../notebooks/past_performance/logistic_analysis_1.ipynb)
   - [Alternative Features Analysis](../notebooks/past_performance/logistic_analysis_2.ipynb)
   - [XGBoost Advanced Analysis](../notebooks/past_performance/xgboost_logistic_analysis_3.ipynb)
5. **Production-Ready Model**: XGBoost with 14 engineered features including DNF handling
6. **Complete Documentation**: This report and extensive inline notebook documentation

---

*Report prepared for: Equibase*  
*Date: October 7, 2025*  
*Author: Tyler Skidmore*  
*Repository: [https://github.com/jQueryousGeorge/RaceLens](https://github.com/jQueryousGeorge/RaceLens)*