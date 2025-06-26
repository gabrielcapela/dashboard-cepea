import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from scripts.utils import get_clean_data 
from scripts.utils import plot_forecast
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
control = True
if "start_date" not in st.session_state:
    st.session_state.start_date = None
if "end_date" not in st.session_state:
    st.session_state.end_date = None




# Sidebar navigation
st.sidebar.title("NAVIGATION")
page = st.sidebar.radio("Go to", ["ℹ️ About", "📈 Visualization", "📋 Data Source & Scraping", "💰 Price Forecast"], label_visibility="collapsed")

# Logic for each page
######################################################-----ABOUT----####################################################################
if page == "ℹ️ About":
    st.header("About this Project")
    st.markdown("""
This project aims to integrate, in a practical and functional way, several skills in **Data Science** and **Software Engineering**, applied to the context of agriculture, more specifically to the **analysis and forecasting of prices of agricultural inputs**.

In a sector as strategic as agriculture, **data science** becomes a powerful ally in **decision-making**. With margins that are often tight and highly sensitive to market variations, producers, cooperatives and marketing agents can benefit greatly from predictive analysis, data automation and interactive interfaces that simplify access to information.

#### Project stages:

- **Automated Web Scraping**: performs daily data collection directly from the [**CEPEA (Center for Advanced Studies on Applied Economics)**](https://www.cepea.org.br/br) website, even without API support, using Selenium to interact with the website interface and obtain updated spreadsheets with input prices.

- **Relational Database**: the collected data is organized and stored in a SQLite database, allowing efficient queries and ensuring integrity and historical traceability.
- **Interactive Data Visualization**: intuitive dashboards are made available with Streamlit, allowing the user to explore time series, identify trends and monitor price variations in a clear and accessible way.
- **Predictive Modeling with Machine Learning**: using XGBoost, the system makes predictions of future prices, offering insights that assist in planning and strategic management.
- **Cloud Infrastructure and Automatic Update**: using Docker and Render.com, the system is automatically updated daily, ensuring that the information displayed is always up to date and available online, with reliability and scalability.

By integrating these technologies, this project not only solves a practical problem — such as predicting the price behavior of agricultural inputs — but also serves as a concrete example of the **modern application of data science** in one of the most important sectors of the economy: the agribusiness.

""")
    

    st.markdown("""
    See the complete project repository on github at this [**link**](https://github.com/gabrielcapela/dashboard-cepea).
                
    This project was developed by **Gabriel Capela**.

    """)



# Add social media icons
    import base64

    def img_to_base64(path):
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    email_icon = img_to_base64("images/icons/email.svg")
    github_icon = img_to_base64("images/icons/github.svg")
    linkedin_icon = img_to_base64("images/icons/linkedin.svg")


    st.markdown(f"""
    <div style="text-align: center; margin-top: 30px; font-size: 0; line-height: 0;">
    <a href="mailto:gabrielcapela@ufms.br" title="Email" style="display:inline-block;">
        <img src="data:image/svg+xml;base64,{email_icon}" alt="Email" width="35" style="vertical-align:middle; margin-right:20px;">
    </a>
    <a href="https://github.com/gabrielcapela" title="GitHub" target="_blank" style="display:inline-block;">
        <img src="data:image/svg+xml;base64,{github_icon}" alt="GitHub" width="35" style="vertical-align:middle; margin-right:20px;">
    </a>
    <a href="https://www.linkedin.com/in/gabrielcapela" title="LinkedIn" target="_blank" style="display:inline-block;">
        <img src="data:image/svg+xml;base64,{linkedin_icon}" alt="LinkedIn" width="35" style="vertical-align:middle;">
    </a>
    </div>
    """, unsafe_allow_html=True)



############################################-----VISUALIZATION-----##############################################################
elif page == "📈 Visualization":



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

    
    
    
   # Control variable to check if the end date is adjusted
    final_date_aux = st.session_state.end_date
    if final_date_aux > max_date:
        final_date_aux = max_date
        control = not control

    #    Date Pickers
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
            # Ensure the end date does not exceed the maximum date in the dataset
            value = final_date_aux.date(),
            min_value = min_date.date(),
            max_value = max_date.date(),
            label_visibility="collapsed"
        )



    # Convert inputs
    start_date = pd.to_datetime(start_input)
    if control == False:
        end_date = pd.to_datetime(st.session_state.end_date)
    else:
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

    with st.expander("🏛️ Data Source: CEPEA"):
        st.markdown("""
        The data used in this project comes from [**CEPEA (Center for Advanced Studies on Applied Economics)**](https://www.cepea.org.br/br), which is affiliated with **ESALQ/USP (Luiz de Queiroz College of Agriculture, University of São Paulo)**. **CEPEA** is one of the most **reliable and widely used sources in Brazi**l for agricultural market price information, offering daily price indicators based on transparent methodologies that reflect real market transactions.

        The dataset includes **daily average prices** for agricultural commodities such as **fattened cattle, rice and coffee**, among others. This allows users to track trends and conduct market analyses with a solid technical foundation.
        """)

    with st.expander("🤖 Automated Scraping Process", expanded=False):
        st.markdown(""" 
        Since **CEPEA** does not provide a public API for direct access to its data, an **automated web scraping** process was implemented to extract and **update the data on a daily basis**.

       **The process involves the following steps**:

        - Automated access to CEPEA's website using the Selenium library to simulate human interaction with the page forms;
        - Selection of the desired parameters (commodity, subtype, daily resolution, and date range);
        - Download of `.xls` files generated by the site with updated data;
        - Conversion and standardization of the downloaded files into the appropriate format;
        - Automatic insertion or update of the data in a local **SQLite database**, ensuring historical integrity;
        - Daily scheduling of the scraping process so that it runs automatically in the production environment (Render.com), without manual intervention.

        This mechanism ensures that the data shown in the dashboard is always up-to-date with the latest information published by CEPEA, promoting reliability and relevance in the analyses.
        """)

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


    with st.expander(" 📉 About the PRICE FORECAST", expanded=False):
        st.markdown("""
        The model uses historical data to estimate **future prices** of agricultural commodities and is **updated daily**, ensuring that the system reflects the latest information available. This dynamic retraining process demonstrates how automation and data pipelines can be effectively structured in a real-world scenario.

        The forecasts, generated using the **XGBoost algorithm**, cover the next 5 days and provide an overview of price developments.

        The price forecast presented in this project does not aim to achieve maximum possible accuracy — which is, by the way, a major challenge when dealing with time series with high variability, such as agricultural commodity prices. Instead, the focus is on demonstrating the **technical capability of integrating a relational database with a machine learning model** that is continuously retrained from **daily updated data**. This approach highlights the practical application of **automated pipelines to feed, train, and serve predictive models** in a robust and scalable manner.
        """)
    selected_product, fig = plot_forecast()
    st.pyplot(fig) 






    























