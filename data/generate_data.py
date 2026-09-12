import pandas as pd
import numpy as np
np.random.seed(42)

products = {
    "Wireless Mouse": ("Electronics", 799),
    "Bluetooth Speaker": ("Electronics", 1999),
    "Yoga Mat": ("Fitness", 899),
    "Running Shoes": ("Fitness", 3499),
    "Coffee Mug": ("Home", 299),
    "Desk Lamp": ("Home", 1299),
    "Notebook Set": ("Stationery", 199),
    "Backpack": ("Fashion", 1899),
    "Water Bottle": ("Fitness", 499),
    "Wall Clock": ("Home", 799),
}
cities = ["Delhi", "delhi", "Mumbai", "Bangalore", "bangalore ", "Pune", "Chennai", "Hyderabad"]

rows = []
order_id = 1001
for i in range(60):
    product = np.random.choice(list(products.keys()))
    category, base_price = products[product]
    price = base_price + np.random.choice([0, 0, 0, -50, 100])
    qty = np.random.randint(1, 5)
    city = np.random.choice(cities)
    date = pd.Timestamp("2026-01-01") + pd.Timedelta(days=int(np.random.randint(0, 180)))
    date_str = date.strftime("%Y-%m-%d") if np.random.rand() > 0.15 else date.strftime("%d/%m/%Y")
    rating = np.random.choice([1,2,3,4,5,np.nan], p=[0.03,0.05,0.12,0.35,0.35,0.10])
    rows.append([order_id, product, category, price, qty, city, date_str, rating])
    order_id += 1

df = pd.DataFrame(rows, columns=["order_id","product","category","price","quantity","customer_city","order_date","rating"])

# inject missing values
for col in ["price", "quantity", "customer_city"]:
    idx = np.random.choice(df.index, size=3, replace=False)
    df.loc[idx, col] = np.nan

# inject duplicate rows
dupes = df.sample(4, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

# inject a couple of price values stored as strings with currency symbol (inconsistent formatting)
df["price"] = df["price"].astype(object)
str_idx = np.random.choice(df.index, size=3, replace=False)
df.loc[str_idx, "price"] = df.loc[str_idx, "price"].apply(lambda x: f"Rs.{x}" if pd.notna(x) else x)

df.to_csv("retail_sales_raw.csv", index=False)
print(df.shape)
print(df.head(10))
