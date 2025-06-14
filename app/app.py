import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from scripts.utils import get_clean_data
import os
import base64


# --- PAGE SETUP ---
st.set_page_config(page_title="CEPEA Price Dashboard", layout="wide")

#BDB76B
#A0522D
#A0522D

# --- STYLE SETTING ---
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #BDB76B !important;
            color: white;
        }

        .stSidebar .stRadio > div {
            flex-direction: column;
            gap: 1.3rem;
        }

        .stSidebar .stRadio > div > label {
            display: flex;
            align-items: center;
            justify-content: left;
            background-color: white !important;
            color: black !important;
            padding: 20px 16px !important;
            border: 1px solid #ccc !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
            min-width: 300px !important;
            max-width: 300px !important;
            text-align: left !important;
            margin: 0 auto !important;
        }

        .stSidebar .stRadio > div > label * {
            font-size: 21px !important;
            font-weight: bold !important;
        }

        .stSidebar .stRadio > div > label[data-selected="true"] {
            background-color: #A0522D !important;
            color: white !important;
            border-color: #A0522D !important;
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
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)





# --- CONNECTION WITH DATABASE ---
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








# Initialize session variables only once per session
if "start_date" not in st.session_state:
    st.session_state.start_date = None
if "end_date" not in st.session_state:
    st.session_state.end_date = None




# Sidebar navigation
st.sidebar.title("NAVIGATION")
page = st.sidebar.radio("Go to", ["📈 Visualization", "📋 Data Source & Scraping", "💰 Price Forecast", "ℹ️ About"], label_visibility="collapsed")

# Logic for each page
############################################-----VISUALIZATION-----##############################################################
if page == "📈 Visualization":



    # Page title adjustment
    st.markdown(
    '<div style="text-align: center;">'
    '<div style="background-color: white; color: black; padding: 0.3rem 1rem; '
    'border-radius: 6px; display: inline-block; margin: auto;font-size: 32px; font-weight: bold;">'
    '📈 Price Line Chart'
    '</div>'
    '</div>',
    unsafe_allow_html=True
    )


   # Get cleaned data and selected product
    data_to_plot, product,  time_res = get_clean_data(df)


    # Minimum and maximum dates according to the database
    min_date = data_to_plot['date'].min()
    max_date = data_to_plot['date'].max()


    # Setting the graph limits
    if  st.session_state.start_date is None:
        st.session_state.start_date = min_date    
    if st.session_state.end_date is None:      
        st.session_state.end_date = max_date
    
    
    #  Date Pickers
    col1, col2 = st.columns(2)
    with col1:
        start_input = st.date_input(
            "Start",
            value = st.session_state.start_date.date(),
            min_value = min_date.date(),
            max_value = max_date.date(),
            label_visibility="collapsed"
        )
    with col2:
        end_input = st.date_input(
            "End",
            value = st.session_state.end_date.date(),
            min_value = min_date.date(),
            max_value = max_date.date(),
            label_visibility="collapsed"
        )



    # Convert inputs
    start_date = pd.to_datetime(start_input)
    end_date = pd.to_datetime(end_input)

    # Save updates
    st.session_state.start_date = start_date
    st.session_state.end_date = end_date

    # Validate range
    if start_date > end_date:
        st.warning("Start date must be before end date.")
        st.stop()

    # Adjust to nearest available date if needed
    while start_date not in data_to_plot['date'].values and start_date > min_date:
        start_date -= pd.Timedelta(days=1)
    while end_date not in data_to_plot['date'].values and end_date > min_date:
        end_date -= pd.Timedelta(days=1)

    # Filter data
    mask = (data_to_plot['date'] >= start_date) & (data_to_plot['date'] <= end_date)
    filtered_data = data_to_plot[mask]

    # User feedback
    if filtered_data.empty:
        st.error("No data available in the selected date range.")
        st.stop()
    elif start_date != st.session_state.start_date or end_date != st.session_state.end_date:
        st.info(f"Adjusted to nearest available data: {start_date.date()} to {end_date.date()}")



    ################## LINE CHART ###########################
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
    ####################################




###############################################-----DATA SOURCE AND SCRAPING-----##########################################################
elif page == "📋 Data Source & Scraping":


    st.markdown(
    '<div style="text-align: center;">'
    '<div style="background-color: white; color: black; padding: 0.3rem 1rem; '
    'border-radius: 6px; display: inline-block; margin: auto;font-size: 32px; font-weight: bold;">'
    'Raw Data'
    '</div>'
    '</div>',
    unsafe_allow_html=True
    )
 
    # Get cleaned data and selected product
    data_to_plot = get_clean_data(df)[0]
    st.dataframe(data_to_plot)  

##################################################-----PRICE FORECAST-----##############################################################
elif page == "💰 Price Forecast":
    st.header("Predictions of the prices")
    st.markdown("""
    This dashboard was built using **Streamlit** and displays historical price data from CEPEA.
;;;;;
                
    """)

######################################################-----ABOUT----####################################################################
elif page == "ℹ️ About":
    st.header("About this App")
    st.markdown("""
    This dashboard was built using **Streamlit** and displays historical price data from CEPEA.

    - Data source: CEPEA database
    - Developer: Gabriel Capela
    """)


    























