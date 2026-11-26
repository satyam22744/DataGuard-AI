
# DataGuard AI

### Autonomous Data Quality & Reliability Intelligence Platform

DataGuard AI is a Python-based data quality intelligence platform designed to profile datasets, detect data quality issues, calculate reliability scores, and provide actionable recommendations.

## Project Objectives

- Automatically profile CSV datasets.
- Detect missing values and duplicate records.
- Identify invalid email and numeric values.
- Detect statistical outliers.
- Identify category inconsistencies.
- Calculate intelligent data quality scores.
- Generate explainable quality reports.

## Technology Stack

- Python
- Pandas
- NumPy
- Regular Expressions
- Git and GitHub

## Project Structure

```text
DataGuard-AI/
│
├── backend/
│   ├── data/
│   ├── engine/
│   │   ├── profiler.py
│   │   ├── quality_checker.py
│   │   └── scoring.py
│   ├── reports/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
├── docs/
├── .gitignore
└── README.md
```

## Current Features

### 1. Dataset Profiling
- Dataset dimensions
- Column information
- Missing-value analysis
- Duplicate analysis
- Statistical summaries

### 2. Data Quality Detection
- Missing-value detection
- Duplicate-record detection
- Email format validation
- Numeric range validation
- IQR-based outlier detection
- Category inconsistency detection

### 3. Intelligent Quality Scoring
- Percentage-based issue impact
- Configurable dimension weights
- Severity-based penalties
- Overall quality rating
- Issue impact explanations

### 4. Adaptive Scoring & Explainability

- Unique affected-record counting within quality dimensions
- Severity-aware adaptive scoring
- Percentage-based impact calculation
- Column-level quality impact analysis
- Explainable issue reports
- Actionable quality recommendations
- Configurable scoring weights

## Current Development Status

- [x] Dataset Profiling Engine
- [x] Data Quality Detection Engine
- [x] Initial Advanced Scoring Engine
- [x] Data Quality Detection Engine
- [x] Adaptive Scoring Improvements
- [ ] Automated Data Cleaning
- [ ] Anomaly Detection
- [ ] Data Drift Detection
- [ ] Interactive Dashboard
- [ ] Automated Testing

## How to Run

Clone the repository:

```bash
git clone https://github.com/satyam22744/DataGuard-AI.git
```

Move into the backend folder:

```bash
cd DataGuard-AI/backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Project Vision

The long-term goal is to develop DataGuard AI into an intelligent data reliability platform that helps users understand, assess, clean, and monitor datasets.

## Author

Satyam Kumar
