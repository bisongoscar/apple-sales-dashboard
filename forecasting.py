import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet  # Ensure you have installed Prophet: pip install prophet

# ---------------------------
# Page Configuration & Styling
# ---------------------------
st.set_page_config(page_title="Apple Sales Dashboard", page_icon="🍎", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        /* Overall page styling */
        body {
            background-color: #f0f2f6;
            color: #333333;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        .reportview-container .main {
            background-color: #f0f2f6;
        }
        
        /* Sidebar styling */
        .css-1d391kg {  
            background-color: #ffffff;
            border-right: 1px solid #e6e6e6;
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
        }

        /* Header styling */
        .main-header {
            text-align: center;
            padding: 20px;
        }
        .main-header h1 {
            font-size: 3em;
            color: #2c3e50; /* Deep navy blue for professional look */
        }

        /* Section title styling */
        .section-title {
            font-size: 2em;
            color: #2c3e50;
            margin-top: 20px;
            margin-bottom: 10px;
            border-bottom: 3px solid #3498db; /* Vibrant blue underline */
            padding-bottom: 5px;
        }

        /* Analysis text styling */
        .analysis-text {
            font-size: 1.1em;
            color: #34495e; /* Darker blue-gray for contrast */
            line-height: 1.6;
        }

        /* Dataframe styling */
        .stDataFrame {
            border: 2px solid #2c3e50;
            border-radius: 5px;
            background-color: #ffffff;
        }

        /* Button styling */
        .stButton>button {
            background-color: #3498db; /* Blue button */
            color: white;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #2980b9; /* Darker blue on hover */
        }

        /* Table header styling */
        .stTable thead {
            background-color: #2c3e50; /* Darker navy header */
            color: white;
            font-weight: bold;
        }

        /* Sidebar header styling */
        .sidebar .sidebar-content h1 {
            color: #2c3e50;
        }

        /* Balloon animation on load */
        @keyframes popIn {
            from { transform: scale(0.8); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        .st-balloons {
            animation: popIn 0.5s ease-in-out;
        }

    </style>
""", unsafe_allow_html=True)

# Page header
st.markdown("<div class='main-header'><h1>🍎 Apple Sales Dashboard</h1></div>", unsafe_allow_html=True)

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("Filters")

# Load dataset
df = pd.read_csv("apple_sales_2024.csv")

selected_region = st.sidebar.multiselect("Select Region", 
                                           options=list(df["Region"].unique()), 
                                           default=list(df["Region"].unique()))
selected_states = st.sidebar.multiselect("Select State", 
                                           options=list(df["State"].unique()), 
                                           default=list(df["State"].unique()))
selected_products = st.sidebar.multiselect(
    "Select Product", 
    options=["iPhone Sales (in million units)", "iPad Sales (in million units)", 
             "Mac Sales (in million units)", "Wearables (in million units)"],
    default=["iPhone Sales (in million units)", "iPad Sales (in million units)", 
             "Mac Sales (in million units)", "Wearables (in million units)"]
)

# ---------------------------
# Tabs for Organized Layout
# ---------------------------
tab_overview, tab_forecast, tab_decisions = st.tabs(["Overview", "Forecasting", "Business Decisions"])

# ===========================
# TAB 1: Overview
# ===========================
with tab_overview:
    st.markdown("<div class='section-title'>Filtered Sales Data</div>", unsafe_allow_html=True)
    
    # Filter data for overview visualizations
    overview_df = df[(df["Region"].isin(selected_region)) & (df["State"].isin(selected_states))].copy()
    if selected_products:
        overview_df["Total Product Sales"] = overview_df[selected_products].sum(axis=1)
        display_columns = ["State", "Region"] + selected_products + ["Total Product Sales"]
        filtered_df = overview_df[display_columns]
    else:
        filtered_df = pd.DataFrame(columns=["State", "Region"])
    
    st.dataframe(filtered_df, use_container_width=True)
    
    if not filtered_df.empty:
        # Total Sales by Region
        st.markdown("<div class='section-title'>Total Apple Product Sales by Region</div>", unsafe_allow_html=True)
        region_sales = overview_df.groupby("Region").sum(numeric_only=True)
        
        with st.spinner("Generating bar chart for total sales by region..."):
            fig, ax = plt.subplots(figsize=(10, 5))
            region_total = region_sales[selected_products].sum(axis=1)
            region_total.plot(kind='bar', color="#3498db", ax=ax)
            ax.set_xlabel("Region")
            ax.set_ylabel("Total Sales (Million Units)")
            ax.set_title("Total Apple Product Sales by Region")
            st.pyplot(fig)
        
        st.markdown("""
        <p class='analysis-text'>
        <strong>Analysis:</strong><br>
        - Greater China and Europe have the highest total sales, indicating strong demand.<br>
        - Rest of Asia and the Americas have moderate sales, suggesting varying market penetration.<br>
        - Japan appears to have lower total sales, which may indicate market saturation or fewer sales opportunities.
        </p>
        """, unsafe_allow_html=True)
        
        # Product Sales Comparison by Region
        st.markdown("<div class='section-title'>Comparison of Apple Product Sales by Region</div>", unsafe_allow_html=True)
        with st.spinner("Generating product sales comparison chart..."):
            fig, ax = plt.subplots(figsize=(10, 5))
            region_sales[selected_products].plot(kind='bar', ax=ax)
            ax.set_xlabel("Region")
            ax.set_ylabel("Sales (Million Units)")
            ax.set_title("Comparison of Apple Product Sales by Region")
            st.pyplot(fig)
        
        st.markdown("""
        <p class='analysis-text'>
        <strong>Analysis:</strong><br>
        - iPhone dominates sales in every region, reinforcing it as Apple’s flagship product.<br>
        - iPad sales are significant in Europe & Greater China, suggesting its popularity for both personal & professional use.<br>
        - Mac sales are relatively lower across all regions, likely due to its higher price point.<br>
        - Wearables have strong numbers, indicating the success of Apple’s ecosystem.
        </p>
        """, unsafe_allow_html=True)
        
        # Top Performing States
        st.markdown("<div class='section-title'>Top 10 States by Total Apple Product Sales</div>", unsafe_allow_html=True)
        with st.spinner("Generating top-performing states chart..."):
            state_sales = overview_df.groupby("State")["Total Product Sales"].sum().sort_values(ascending=False).head(10)
            fig, ax = plt.subplots(figsize=(10, 5))
            state_sales.plot(kind="bar", color="#2ecc71", ax=ax)
            ax.set_xlabel("State")
            ax.set_ylabel("Total Sales (Million Units)")
            ax.set_title("Top 10 States by Total Apple Product Sales")
            st.pyplot(fig)
        
        st.markdown("""
        <p class='analysis-text'>
        <strong>Analysis:</strong><br>
        - The top-performing states are concentrated in high-income regions.<br>
        - Chongqing, Shanghai, and major European markets (e.g., Germany, UK) appear frequently, reinforcing the importance of these economic hubs.<br>
        - The U.S. shows multiple top-performing states, underscoring its importance as a key market.
        </p>
        """, unsafe_allow_html=True)
    else:
        st.info("No data available to display charts and analysis based on the current filters.")

# ===========================
# TAB 2: Forecasting
# ===========================
with tab_forecast:
    st.markdown("<div class='section-title'>Sales Forecasting</div>", unsafe_allow_html=True)
    forecast_horizon = st.slider("Select forecast horizon (months)", min_value=1, max_value=12, value=3)
    
    if "Date" in df.columns:
        forecast_df = df[(df["Region"].isin(selected_region)) & (df["State"].isin(selected_states))].copy()
        if selected_products:
            forecast_df["Total Product Sales"] = forecast_df[selected_products].sum(axis=1)
            forecast_df["Date"] = pd.to_datetime(forecast_df["Date"])
            # Aggregate data by month
            time_series = forecast_df.groupby(pd.Grouper(key='Date', freq='M'))["Total Product Sales"].sum().reset_index()
            time_series.rename(columns={"Date": "ds", "Total Product Sales": "y"}, inplace=True)
            
            if time_series.empty:
                st.info("No data available for forecasting based on current filters.")
            else:
                with st.spinner("Fitting forecast model..."):
                    model = Prophet()
                    model.fit(time_series)
                    future = model.make_future_dataframe(periods=forecast_horizon, freq='M')
                    forecast = model.predict(future)
                
                st.markdown("<div class='section-title'>Forecasted Total Product Sales</div>", unsafe_allow_html=True)
                fig1 = model.plot(forecast)
                st.pyplot(fig1)
                
                st.markdown("<div class='section-title'>Forecast Components</div>", unsafe_allow_html=True)
                fig2 = model.plot_components(forecast)
                st.pyplot(fig2)
        else:
            st.warning("Please select at least one product for forecasting.")
    else:
        st.error("No 'Date' column found in dataset for forecasting.")

# ===========================
# TAB 3: Business Decisions
# ===========================
with tab_decisions:
    st.markdown("<div class='section-title'>Supporting Business Decisions</div>", unsafe_allow_html=True)
    st.markdown("""
    <p class='analysis-text'>
    <strong>Marketing Strategy Recommendations:</strong><br>
    - Focus ad spending on Greater China and Europe, the highest-performing markets.<br>
    - Promote iPads heavily in professional and student sectors.<br>
    - Utilize influencers and digital advertising for wearables.
    </p>
    <p class='analysis-text'>
    <strong>Product Development Strategy:</strong><br>
    - Prioritize innovation in iPhones and wearables.<br>
    - Introduce more affordable Mac models to expand reach.<br>
    - Invest in expanding Apple’s digital services for long-term growth.
    </p>
    <p class='analysis-text'>
    <strong>Resource Allocation Strategy:</strong><br>
    - Increase manufacturing and retail investment in top-performing regions.<br>
    - Expand cloud infrastructure and AI-driven services.<br>
    - Optimize costs in underperforming markets like Japan.
    </p>
    <p class='analysis-text'>
    <strong>Conclusion:</strong><br>
    - Apple’s future strategy should integrate <strong>stronger AI and battery improvements</strong> for iPhones.<br>
    - Services revenue is a major driver; hence, investments in <strong>Apple One, Apple Music, and iCloud</strong> should increase.<br>
    - <strong>Wearables and iPads present strong opportunities for growth</strong>, particularly in professional markets.
    </p>
    """, unsafe_allow_html=True)

# ---------------------------
# Fun Effects
# ---------------------------
# Trigger a celebratory effect (balloons) after the dashboard loads
st.balloons()