import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

# Product labels for display
product_labels = {
    'fattened_cattle': 'Fattened Cattle',
    'rice': 'Rice',
    'coffee': 'Coffee'
}


def get_clean_data(df):
    """
    Display commodity and time resolution selectors, return cleaned and optionally resampled data.

    Args:
        df (pd.DataFrame): Original DataFrame with 'date' and commodity columns.

    Returns:
        product (str): Selected commodity
        data_to_plot (pd.DataFrame): DataFrame with date and selected product, possibly resampled
        time_res (str): Selected time resolution
    """

    # Vertical spacing
    st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
    # Commodity selection title
    st.markdown(
        '<div style="text-align: left;">'
        '<div style="background-color: white; color: black; padding: 0.3rem 1rem; '
        'border-radius: 6px; display: inline-block; font-size: 20px;">'
        'Select a commodity:'
        '</div></div>',
        unsafe_allow_html=True
    )

    ############ Adjusting the product selection ####################
    if "selected_product" not in st.session_state:
        st.session_state.selected_product = list(product_labels.keys())[0]
    cols = st.columns(len(product_labels))
    for idx, (key, label) in enumerate(product_labels.items()):
        with cols[idx]:
            image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images", f"{key}.jpg"))
            if os.path.exists(image_path):
                st.image(image_path, width=400)
            if st.button(label, key=f"btn_{key}"):
                st.session_state.selected_product = key
    selected_product = st.session_state.selected_product
    ##############################################

    # Vertical spacing
    st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
    # Time resolution selector title
    st.markdown(
        '<div style="text-align: left;">'
        '<div style="background-color: white; color: black; padding: 0.3rem 1rem; '
        'border-radius: 6px; display: inline-block; font-size: 20px;">'
        'Select time resolution:'
        '</div></div>',
        unsafe_allow_html=True
    )

    ############ Adjusting the time resolution selection ##############
    time_res = st.selectbox("Select time resolution:", ["Daily", "Monthly", "Yearly"], label_visibility="collapsed")
    # Checks and resets dates if there was a change in resolution
    if "time_res" not in st.session_state:
        st.session_state.time_res = time_res
    elif time_res != st.session_state.time_res:
        st.session_state.time_res = time_res
    ##########################################

    # Clean and prepare data according to selected parameters
    df['date'] = pd.to_datetime(df['date'])

    df_clean = df[['date', selected_product]].dropna()

    if time_res == "Monthly":
        df_clean = df_clean.set_index('date').resample('MS').mean().reset_index()
    elif time_res == "Yearly":
        df_clean = df_clean.set_index('date').resample('YS').mean().reset_index()



    return  df_clean, selected_product, time_res




# def plot_forecast(n_past=20, n_future=5):
#     """
#     Displays an interactive commodity selection with images and returns a chart showing
#     historical prices and forecasted values using CSV data.

#     Parameters:
#         n_past (int): Number of past days to display.
#         n_future (int): Number of future days to forecast.

#     Returns:
#         selected_product (str): Selected product name.
#         fig (matplotlib.figure.Figure): Forecast plot (use with st.pyplot(fig)).
#     """

#     # Aesthetic spacing
#     st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)

#     # Styled section title
#     st.markdown(
#         '<div style="text-align: left;">'
#         '<div style="background-color: white; color: black; padding: 0.3rem 1rem; '
#         'border-radius: 6px; display: inline-block; font-size: 20px;">'
#         'Select a commodity:'
#         '</div></div>',
#         unsafe_allow_html=True
#     )

#     # Default selected product (if not set)
#     if "selected_product" not in st.session_state:
#         st.session_state.selected_product = list(product_labels.keys())[0]

#     # Create columns with images and buttons for each product
#     cols = st.columns(len(product_labels))
#     for idx, (key, label) in enumerate(product_labels.items()):
#         with cols[idx]:
#             image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images", f"{key}.jpg"))
#             if os.path.exists(image_path):
#                 st.image(image_path, width=300)
#             if st.button(label, key=f"btn_{key}"):
#                 st.session_state.selected_product = key

#     selected_product = st.session_state.selected_product

#     # Load forecast CSV
#     path = os.path.join("data", "plot_data", f"{selected_product}_forecast.csv")
#     if not os.path.exists(path):
#         st.error(f"File not found: {path}")
#         return selected_product, None

#     df = pd.read_csv(path, parse_dates=['ds'])

#     # Check if there is enough data
#     if len(df) < n_past + n_future:
#         st.error("Not enough data to generate the chart.")
#         return selected_product, None

#     # Split into recent and future data
#     df_recent = df.iloc[:n_past].copy()
#     df_future = df.iloc[n_past:].copy()

#     # Plot creation
#     fig, ax = plt.subplots(figsize=(10, 5))
#     ax.plot(df_recent['ds'], df_recent['y'], marker='o', label='Historical', color='blue')
#     ax.plot(df_future['ds'], df_future['y'], marker='o', linestyle='--', label='Forecast', color='orange')
#     ax.axvline(x=df_recent['ds'].iloc[-1], color='gray', linestyle='--', label='Forecast Start')
#     ax.set_title(f"{selected_product.replace('_', ' ').title()} — Last {n_past} Days + {n_future} Day Forecast")
#     ax.set_xlabel("Date")
#     ax.set_ylabel("Price")
#     ax.tick_params(axis='x', rotation=45)
#     ax.grid(True)
#     ax.legend()
#     fig.tight_layout()

#     return selected_product, fig


import pandas as pd
import matplotlib.pyplot as plt
import os
import psycopg2
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

def plot_forecast(n_past=20, n_future=5):
    

    # Styled commodity selection
    st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align: left;">'
        '<div style="background-color: white; color: black; padding: 0.3rem 1rem; '
        'border-radius: 6px; display: inline-block; font-size: 20px;">'
        'Select a commodity:'
        '</div></div>',
        unsafe_allow_html=True
    )

    if "selected_product" not in st.session_state:
        st.session_state.selected_product = list(product_labels.keys())[0]

    cols = st.columns(len(product_labels))
    for idx, (key, label) in enumerate(product_labels.items()):
        with cols[idx]:
            image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images", f"{key}.jpg"))
            if os.path.exists(image_path):
                st.image(image_path, width=300)
            if st.button(label, key=f"btn_{key}"):
                st.session_state.selected_product = key

    selected_product = st.session_state.selected_product

    # Connect to PostgreSQL and fetch forecast data
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", 5432)
        )
        query = f"""
            SELECT ds, y FROM plot_data
            WHERE commodity = %s
            ORDER BY ds
        """
        df = pd.read_sql(query, conn, params=(selected_product,))
        conn.close()
    except Exception as e:
        st.error(f"Database error: {e}")
        return selected_product, None

    if len(df) < n_past + n_future:
        st.error("Not enough data to generate the chart.")
        return selected_product, None

    df['ds'] = pd.to_datetime(df['ds'])
    df = df.sort_values('ds')
    df_recent = df.iloc[:n_past].copy()
    df_future = df.iloc[n_past:].copy()

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_recent['ds'], df_recent['y'], marker='o', label='Historical', color='blue')
    ax.plot(df_future['ds'], df_future['y'], marker='o', linestyle='--', label='Forecast', color='orange')
    ax.axvline(x=df_recent['ds'].iloc[-1], color='gray', linestyle='--', label='Forecast Start')
    ax.set_title(f"{selected_product.replace('_', ' ').title()} — Last {n_past} Days + {n_future} Day Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    ax.legend()
    fig.tight_layout()

    return selected_product, fig
