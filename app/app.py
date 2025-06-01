import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from scripts.utils import get_clean_data
import os


# --- PAGE SETUP ---
st.set_page_config(page_title="CEPEA Price Dashboard", layout="wide")



# --- STYLE SETTING ---
st.markdown("""
    <style>
        /* Leaves the st.radio buttons stacked vertically and taking up the entire width */
        .stRadio > div {
            flex-direction: column;
        }

        .stRadio > div > label {
            border: 1px solid #ccc;
            padding: 10px 15px;
            border-radius: 5px;
            margin-bottom: 5px;
            text-align: center;
            width: 100%;
            transition: all 0.2s;
            background-color: #f5f5f5;
            font-weight: 500;
        }

        .stRadio > div > label:hover {
            background-color: #e0e0e0;
        }

        .stRadio > div > label[data-selected="true"] {
            background-color: #A0522D;
            color: white;
            border-color: #A0522D;
        }
    </style>
""", unsafe_allow_html=True)




# ---HEADER---
# Custom fixed header with sidebar-aware layout
st.markdown("""
    <style>
        /* Full-width fixed header */
        .custom-header {
            position: fixed;
            top: 60px;
            left: 0;
            width: 100%;
            height: 70px;
            background-color: #A0522D;
            z-index: 1001;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.3);
        }

        .custom-header h1 {
            color: white;
            font-size: 42px;
            margin: 0;
        }

    </style>

    <div class="custom-header">
        <h1>📊 CEPEA Price Dashboard</h1>
    </div>
""", unsafe_allow_html=True)




# Add vertical space manually after header
st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True)










# Get the path to the current directory (where app.py is)
base_dir = os.path.dirname(__file__)

# Build the full path to the database
db_path = os.path.join(base_dir, "data", "cepea.db")

# Connect to the database
conn = sqlite3.connect(db_path)

# Load all records from the 'prices' table
df = pd.read_sql("SELECT * FROM prices ORDER BY date", conn)

# Close the database connection
conn.close()











# Sidebar navigation
st.sidebar.title("NAVIGATION")
page = st.sidebar.radio("Go to", ["📈 Visualization", "📋 Data Source & Scraping", "💰 Price Forecast", "ℹ️ About"])

# Logic for each page
if page == "📈 Visualization":

    st.header("Price Chart")
    st.write("This section will show the line chart of selected commodity.")

    # Get cleaned data and selected product
    product, data_to_plot = get_clean_data(df)



    # --- DATE RANGE SELECTOR WITH STATE ---
    min_date = data_to_plot['date'].min()
    max_date = data_to_plot['date'].max()

    # Initialize session_state only once
    if "start_date" not in st.session_state:
        st.session_state.start_date = min_date
    if "end_date" not in st.session_state:
        st.session_state.end_date = max_date

    # Ensure that saved dates are within the current dataset limits
    saved_start = st.session_state.start_date
    saved_end = st.session_state.end_date

    # Corrects out-of-range values
    if saved_start < min_date:
        saved_start = min_date
    if saved_start > max_date:
        saved_start = max_date

    if saved_end > max_date:
        saved_end = max_date
    if saved_end < min_date:
        saved_end = min_date

    # Show selectors with values ​​already set
    start_input = st.date_input("Start date:", value=saved_start.date(), min_value=min_date.date(), max_value=max_date.date())
    end_input = st.date_input("End date:", value=saved_end.date(), min_value=min_date.date(), max_value=max_date.date())


    # Convert to datetime
    start_date = pd.to_datetime(start_input)
    end_date = pd.to_datetime(end_input)

    # Save updated selections
    st.session_state.start_date = start_date
    st.session_state.end_date = end_date

    # Check validity
    if start_date > end_date:
        st.warning("Start date must be before end date.")
        st.stop()

    # Adjust to closest available date
    while start_date not in data_to_plot['date'].values and start_date > min_date:
        start_date -= pd.Timedelta(days=1)
    while end_date not in data_to_plot['date'].values and end_date > min_date:
        end_date -= pd.Timedelta(days=1)

    # Filter the data
    mask = (data_to_plot['date'] >= start_date) & (data_to_plot['date'] <= end_date)
    filtered_data = data_to_plot[mask]

    # Feedback to user
    if filtered_data.empty:
        st.error("No data available in the selected date range.")
        st.stop()
    elif start_date != st.session_state.start_date or end_date != st.session_state.end_date:
        st.info(f"Adjusted to nearest available data: {start_date.date()} to {end_date.date()}")





    # CREATE THE LINE CHART
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(filtered_data['date'], filtered_data[product], marker='o')


    # Customize the plot
    ax.set_title(f'{product.replace("_", " ").title()} Price Over Time', fontsize=20)
    ax.set_xlabel('Date', fontsize=20, labelpad=10)
    ax.set_ylabel('Price', fontsize=20, labelpad=10)
    ax.tick_params(axis='both', labelsize=12) 
    ax.grid(True) 

    # Remove top and right border (spines)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)





elif page == "📋 Data Source & Scraping":
    st.header("Raw Data")
    # 👉 Aqui vai o st.dataframe com os dados
    st.write("This section will display the raw data table.")


    # Optional: display the filtered data table
    st.caption("Price history for selected commodity")
    # Get cleaned data and selected product
    data_to_plot = get_clean_data(df)[1]
    st.dataframe(data_to_plot)  


elif page == "💰 Price Forecast":
    st.header("Predictions of the prices")
    st.markdown("""
    This dashboard was built using **Streamlit** and displays historical price data from CEPEA.
;;;;;
                
    """)


elif page == "ℹ️ About":
    st.header("About this App")
    st.markdown("""
    This dashboard was built using **Streamlit** and displays historical price data from CEPEA.

    - Data source: CEPEA database
    - Developer: Gabriel Capela
    """)


    























