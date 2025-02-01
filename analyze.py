import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("apple_sales_2024.csv")

# Aggregate sales data by region
region_sales = df.groupby("Region").sum(numeric_only=True)

# Plot total sales distribution by region
plt.figure(figsize=(12, 6))
region_sales[['iPhone Sales (in million units)', 'iPad Sales (in million units)',
              'Mac Sales (in million units)', 'Wearables (in million units)']].sum(axis=1).plot(kind='bar')
plt.title("Total Apple Product Sales by Region")
plt.ylabel("Total Sales (Million Units)")
plt.xlabel("Region")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# Plot product sales comparison
plt.figure(figsize=(12, 6))
region_sales[['iPhone Sales (in million units)', 'iPad Sales (in million units)',
              'Mac Sales (in million units)', 'Wearables (in million units)']].plot(kind='bar', figsize=(12, 6))
plt.title("Comparison of Apple Product Sales by Region")
plt.ylabel("Sales (Million Units)")
plt.xlabel("Region")
plt.xticks(rotation=45)
plt.legend(title="Product Category")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# Calculate total product sales
df["Total Product Sales"] = df[['iPhone Sales (in million units)', 'iPad Sales (in million units)',
                                'Mac Sales (in million units)', 'Wearables (in million units)']].sum(axis=1)

# Scatter plot of Total Product Sales vs. Services Revenue
plt.figure(figsize=(10, 6))
plt.scatter(df["Total Product Sales"], df["Services Revenue (in billion $)"], alpha=0.5, color='blue')
plt.title("Total Product Sales vs. Services Revenue")
plt.xlabel("Total Product Sales (Million Units)")
plt.ylabel("Services Revenue (Billion $)")
plt.grid(True, linestyle="--", alpha=0.7)
plt.show()

# Aggregate total sales by state
state_sales = df.groupby("State")["Total Product Sales"].sum().sort_values(ascending=False).head(10)

# Plot top 10 performing states by total sales
plt.figure(figsize=(12, 6))
state_sales.plot(kind="bar", color="green")
plt.title("Top 10 States by Total Apple Product Sales")
plt.ylabel("Total Sales (Million Units)")
plt.xlabel("State")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
