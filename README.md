# Hands-On Data Lab Implementation

Task 2 of the Data Science internship program. A complete, working Data
Science environment exercised end-to-end on a simulated retail sales
dataset: setup, data loading, cleaning, Pandas/NumPy manipulation,
visualization, and basic analysis.

## Contents

- `Hands_On_Data_Lab_Implementation.ipynb` — main notebook (fully executed,
  outputs included)
- `data/retail_sales_raw.csv` — raw dataset with intentional data-quality
  issues (missing values, duplicates, inconsistent formats)
- `data/city_region_lookup.csv` — lookup table used to demonstrate merging
- `data/retail_sales_cleaned.csv` — cleaned dataset produced by the notebook
- `data/generate_data.py` — script used to generate the raw sample dataset
- `*.png` — charts exported by the notebook (bar, line, histogram, scatter,
  box plot, correlation heatmap)
- `requirements.txt` — Python dependencies

## Topics covered

1. Environment setup — Python, Jupyter, NumPy, Pandas, Matplotlib, Seaborn,
   Scikit-learn
2. Pandas & NumPy — selection, filtering, sorting, grouping, aggregation,
   merging, transformation, numerical operations
3. Data cleaning — missing values, duplicate records, inconsistent
   formatting, incorrect data types
4. Visualization — bar chart, line chart, histogram, scatter plot, box plot
5. Basic analysis — descriptive statistics, distributions, correlation

## How to run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
jupyter notebook Hands_On_Data_Lab_Implementation.ipynb
```

## Author

_<your name here>_
