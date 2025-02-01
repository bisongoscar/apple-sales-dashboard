import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("apple_sales_2024.csv")

# Sidebar Filters
st.sidebar.header("Filters")
selected_region = st.sidebar.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())
selected_states = st.sidebar.multiselect("Select State", df["State"].unique(), default=df["State"].unique())
selected_products = st.sidebar.multiselect("Select Product", ["iPhone Sales (in million units)", "iPad Sales (in million units)", "Mac Sales (in million units)", "Wearables (in million units)"], default=["iPhone Sales (in million units)", "iPad Sales (in million units)", "Mac Sales (in million units)", "Wearables (in million units)"])

# Filter data based on selection
filtered_df = df[df["Region"].isin(selected_region) & df["State"].isin(selected_states)]

if selected_products:
    filtered_df["Total Product Sales"] = filtered_df[selected_products].sum(axis=1)
    display_columns = ["State", "Region"] + selected_products + ["Total Product Sales"]
    filtered_df = filtered_df[display_columns]
else:
    filtered_df = pd.DataFrame(columns=["State", "Region"])

# Display filtered data
st.write("### Filtered Sales Data")
st.dataframe(filtered_df)

if not filtered_df.empty:
    # Total Sales by Region
    st.write("### Total Apple Product Sales by Region")
    region_sales = filtered_df.groupby("Region").sum(numeric_only=True)
    fig, ax = plt.subplots()
    region_sales[selected_products].sum(axis=1).plot(kind='bar', ax=ax)
    ax.set_xlabel("Region")
    ax.set_ylabel("Total Sales (Million Units)")
    ax.set_title("Total Apple Product Sales by Region")
    st.pyplot(fig)

    # Product Sales Comparison
    st.write("### Comparison of Apple Product Sales by Region")
    fig, ax = plt.subplots()
    region_sales[selected_products].plot(kind='bar', ax=ax)
    ax.set_xlabel("Region")
    ax.set_ylabel("Sales (Million Units")
    ax.set_title("Comparison of Apple Product Sales by Region")
    st.pyplot(fig)

    # Scatter plot of Total Product Sales vs. Services Revenue
    st.write("### Total Product Sales vs. Services Revenue")
    fig, ax = plt.subplots()
    ax.scatter(filtered_df["Total Product Sales"], df.loc[filtered_df.index, "Services Revenue (in billion $)"], alpha=0.5, color='blue')
    ax.set_xlabel("Total Product Sales (Million Units)")
    ax.set_ylabel("Services Revenue (Billion $)")
    ax.set_title("Total Product Sales vs. Services Revenue")
    st.pyplot(fig)

    # Top Performing States
    st.write("### Top 10 States by Total Apple Product Sales")
    state_sales = filtered_df.groupby("State")["Total Product Sales"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    state_sales.plot(kind="bar", ax=ax, color="green")
    ax.set_xlabel("State")
    ax.set_ylabel("Total Sales (Million Units)")
    ax.set_title("Top 10 States by Total Apple Product Sales")
    st.pyplot(fig)

# Run the app with: streamlit run your_script.py
