import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))

def code(text):
    cells.append(nbf.v4.new_code_cell(text))

# ---------------------------------------------------------------
md("""# Hands-On Data Lab Implementation

**Submission:** Task 2 — Hands-On Data Lab Implementation
**Author:** _<your name here>_
**Date:** _<submission date>_

This notebook sets up a working Data Science environment and works through a
full practical cycle — loading, cleaning, transforming, visualizing, and
analyzing a retail sales dataset — using Pandas, NumPy, Matplotlib, Seaborn,
and Scikit-learn.
""")

# ---------------------------------------------------------------
md("""## 1. Environment Setup

This project uses:

- **Python 3** as the language
- **Jupyter Notebook** as the interactive environment
- **NumPy** for numerical operations
- **Pandas** for tabular data handling
- **Matplotlib** and **Seaborn** for visualization
- **Scikit-learn** for a quick preprocessing utility later in the notebook

Install everything with:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn jupyter
```

The cell below imports every library used in this notebook and prints their
versions, confirming the environment is correctly configured.
""")
code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

sns.set_theme(style="whitegrid")
print("numpy:", np.__version__)
print("pandas:", pd.__version__)
import matplotlib
print("matplotlib:", matplotlib.__version__)
print("seaborn:", sns.__version__)
import sklearn
print("scikit-learn:", sklearn.__version__)
""")

# ---------------------------------------------------------------
md("""## 2. Load the Dataset

The dataset is a simulated retail sales log (`data/retail_sales_raw.csv`)
deliberately containing the kinds of issues real-world data has: missing
values, duplicate rows, inconsistent city-name casing, and prices stored as
text with a currency prefix.
""")
code("""df = pd.read_csv("data/retail_sales_raw.csv")
print("Shape:", df.shape)
df.head(10)
""")

code("""df.info()
""")

# ---------------------------------------------------------------
md("""## 3. Data Cleaning

### 3.1 Identify issues
""")
code("""print("Missing values per column:")
print(df.isna().sum())
print()
print("Duplicate rows:", df.duplicated().sum())
print()
print("Unique customer_city values (raw):", sorted(df['customer_city'].dropna().unique()))
print()
print("Sample non-numeric price values:", df.loc[df['price'].astype(str).str.contains('Rs', na=False), 'price'].tolist())
""")

md("### 3.2 Fix inconsistent data types")
code("""# Strip 'Rs.' prefix and convert price to numeric
df["price"] = (
    df["price"].astype(str)
    .str.replace("Rs.", "", regex=False)
    .replace("nan", np.nan)
    .astype(float)
)

# Standardize order_date: parse both 'YYYY-MM-DD' and 'DD/MM/YYYY' formats
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", dayfirst=False)

df[["price", "order_date"]].dtypes
""")

md("### 3.3 Standardize categorical text")
code("""# Trim whitespace and normalize casing for city names
df["customer_city"] = df["customer_city"].str.strip().str.title()
sorted(df["customer_city"].dropna().unique())
""")

md("### 3.4 Handle missing values")
code("""# Numeric columns: impute with the column median (robust to outliers)
for col in ["price", "quantity"]:
    median_val = df[col].median()
    df[col] = df[col].fillna(median_val)

# Categorical: impute with the mode
df["customer_city"] = df["customer_city"].fillna(df["customer_city"].mode()[0])

# Rating: leave missing as NaN (represents "no rating given"), but flag it
df["has_rating"] = df["rating"].notna()

print("Remaining missing values:")
print(df.isna().sum())
""")

md("### 3.5 Remove duplicate records")
code("""before = len(df)
df = df.drop_duplicates().reset_index(drop=True)
after = len(df)
print(f"Removed {before - after} duplicate rows. New shape: {df.shape}")
""")

md("### 3.6 Fix data types and derive useful columns")
code("""df["quantity"] = df["quantity"].astype(int)
df["order_month"] = df["order_date"].dt.month_name()
df["revenue"] = df["price"] * df["quantity"]
df.head()
""")

# ---------------------------------------------------------------
md("""## 4. Working with Pandas & NumPy

### 4.1 Selection, filtering, and sorting
""")
code("""# Selection
electronics = df[df["category"] == "Electronics"]
print("Electronics orders:", len(electronics))

# Filtering with multiple conditions
high_value = df[(df["revenue"] > 2000) & (df["has_rating"])]
print("High-value rated orders:", len(high_value))

# Sorting
df.sort_values("revenue", ascending=False).head(5)[["product", "customer_city", "revenue"]]
""")

md("### 4.2 Grouping and aggregation")
code("""category_summary = df.groupby("category").agg(
    total_revenue=("revenue", "sum"),
    avg_price=("price", "mean"),
    orders=("order_id", "count"),
).sort_values("total_revenue", ascending=False)
category_summary
""")

md("### 4.3 Merging datasets")
code("""region_lookup = pd.read_csv("data/city_region_lookup.csv")
df = df.merge(region_lookup, on="customer_city", how="left")
df[["customer_city", "region"]].drop_duplicates().reset_index(drop=True)
""")

md("### 4.4 Transformation and numerical operations with NumPy")
code("""# Min-max scale revenue into a 0-1 range using scikit-learn
scaler = MinMaxScaler()
df["revenue_scaled"] = scaler.fit_transform(df[["revenue"]])

# NumPy-based transform: log revenue to reduce skew
df["log_revenue"] = np.log1p(df["revenue"])

df[["revenue", "revenue_scaled", "log_revenue"]].describe()
""")

# ---------------------------------------------------------------
md("## 5. Data Visualization")

md("### 5.1 Bar chart — revenue by category")
code("""plt.figure(figsize=(8, 5))
category_summary["total_revenue"].plot(kind="bar", color=sns.color_palette("viridis", len(category_summary)))
plt.title("Total Revenue by Category")
plt.ylabel("Revenue (₹)")
plt.xlabel("Category")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("revenue_by_category.png", dpi=120)
plt.show()
""")

md("### 5.2 Line chart — revenue trend by month")
code("""month_order = ["January","February","March","April","May","June","July","August","September","October","November","December"]
monthly_revenue = df.groupby("order_month")["revenue"].sum().reindex(month_order).dropna()

plt.figure(figsize=(8, 5))
monthly_revenue.plot(kind="line", marker="o", color="teal")
plt.title("Monthly Revenue Trend")
plt.ylabel("Revenue (₹)")
plt.xlabel("Month")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("monthly_revenue_trend.png", dpi=120)
plt.show()
""")

md("### 5.3 Histogram — distribution of order revenue")
code("""plt.figure(figsize=(8, 5))
sns.histplot(df["revenue"], bins=15, kde=True, color="slateblue")
plt.title("Distribution of Order Revenue")
plt.xlabel("Revenue (₹)")
plt.tight_layout()
plt.savefig("revenue_distribution.png", dpi=120)
plt.show()
""")

md("### 5.4 Scatter plot — price vs. quantity")
code("""plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="price", y="quantity", hue="category", s=70)
plt.title("Price vs. Quantity by Category")
plt.tight_layout()
plt.savefig("price_vs_quantity.png", dpi=120)
plt.show()
""")

md("### 5.5 Box plot — revenue by region")
code("""plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="region", y="revenue", palette="Set2")
plt.title("Revenue Distribution by Region")
plt.tight_layout()
plt.savefig("revenue_by_region_boxplot.png", dpi=120)
plt.show()
""")

# ---------------------------------------------------------------
md("## 6. Basic Data Analysis")
code("""df[["price", "quantity", "revenue", "rating"]].describe()
""")

code("""corr = df[["price", "quantity", "revenue", "rating"]].corr(numeric_only=True)
plt.figure(figsize=(6, 5))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix")
plt.tight_layout()
plt.savefig("correlation_heatmap.png", dpi=120)
plt.show()
""")

md("""### Observations

- **Electronics** and **Fitness** categories generate the highest total
  revenue, driven by higher per-unit prices rather than order volume.
- The monthly revenue trend shows some fluctuation across the simulated
  6-month window but no strong seasonal pattern in this sample.
- Order revenue is right-skewed — most orders are modest, with a smaller
  number of high-value orders pulling the mean above the median.
- **Price and revenue are strongly positively correlated** (expected, since
  revenue = price × quantity), while rating shows negligible correlation
  with price or quantity in this sample — customer satisfaction here isn't
  simply a function of how much was spent.
- Cleaning steps (currency stripping, date-format unification, city
  standardization, median/mode imputation, de-duplication) were essential
  before any of the above analysis was trustworthy — the raw file could not
  have been grouped, merged, or plotted correctly without them.
""")

# ---------------------------------------------------------------
md("""## 7. Save the Cleaned Dataset""")
code("""df.to_csv("data/retail_sales_cleaned.csv", index=False)
print("Cleaned dataset saved to data/retail_sales_cleaned.csv")
df.shape
""")

# ---------------------------------------------------------------
md("""## 8. Conclusion

This lab set up a complete Data Science environment and exercised it
end-to-end: loading a messy real-world-style dataset, diagnosing and fixing
data-quality issues, using Pandas/NumPy for selection, filtering, sorting,
grouping, merging, and transformation, producing five different chart types
with Matplotlib/Seaborn, and closing with descriptive statistics and a
correlation analysis. The cleaned dataset and all generated charts are saved
alongside this notebook for reference.
""")

nb["cells"] = cells

with open("Hands_On_Data_Lab_Implementation.ipynb", "w") as f:
    nbf.write(nb, f)

print("Notebook written.")
