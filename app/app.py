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










# Connect to the SQLite database
conn = sqlite3.connect("data/cepea.db")

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

    # Create the line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data_to_plot['date'], data_to_plot[product], marker='o')

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


    

    st.write("Test loading image")
    image_path = os.path.join("images", "coffee.jpg")
    st.write("Image path:", image_path)

    if os.path.exists(image_path):
        st.image(image_path, caption="Test Coffee Image", width=150)
    else:
        st.error("Image not found!")





















