import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from scripts.utils import get_clean_data

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
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["📈 Price Chart", "📋 Raw Data", "ℹ️ About"])

# Logic for each page
if page == "📈 Price Chart":

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





elif page == "📋 Raw Data":
    st.header("Raw Data")
    # 👉 Aqui vai o st.dataframe com os dados
    st.write("This section will display the raw data table.")


    # Optional: display the filtered data table
    st.caption("Price history for selected commodity")
    # Get cleaned data and selected product
    data_to_plot = get_clean_data(df)[1]
    st.dataframe(data_to_plot)  

elif page == "ℹ️ About":
    st.header("About this App")
    st.markdown("""
    This dashboard was built using **Streamlit** and displays historical price data from CEPEA.

    - Data source: CEPEA database
    - Developer: Gabriel Capela
    """)





















