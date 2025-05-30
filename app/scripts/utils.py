import pandas as pd
import streamlit as st
import os

# Product labels for display
product_labels = {
    'fattened_cattle': 'Fattened Cattle',
    'rice': 'Rice',
    'coffee': 'Coffee',
    'dollar': 'Dollar'
}

def get_clean_data(df):
    """
    Display commodity and time resolution selectors, return cleaned and optionally resampled data.

    Args:
        df (pd.DataFrame): Original DataFrame with 'date' and commodity columns.

    Returns:
        product (str): Selected commodity
        data_to_plot (pd.DataFrame): DataFrame with date and selected product, possibly resampled
    """

    st.markdown("### Select a commodity")

    # Create 4 columns (1 for each product)
    cols = st.columns(len(product_labels))
    selected_product = None

    for idx, (key, label) in enumerate(product_labels.items()):
        with cols[idx]:
            # Absolute path relative to this file (utils.py inside /app/scripts/)
            image_path = os.path.join(os.path.dirname(__file__), "..", "images", f"{key}.jpg")
            image_path = os.path.abspath(image_path)
            if os.path.exists(image_path):
                st.image(image_path, width=400)
            if st.button(label, key=key):
                selected_product = key

    # Use default if none selected
    if selected_product is None:
        selected_product = list(product_labels.keys())[0]

    # Time resolution selector
    time_res = st.radio("Select time resolution", ["Daily", "Monthly", "Yearly"], horizontal=True)

    # Clean and prepare data
    df['date'] = pd.to_datetime(df['date'])
    df[selected_product] = pd.to_numeric(
        df[selected_product].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False),
        errors='coerce'
    )

    df_clean = df[['date', selected_product]].dropna()

    if time_res == "Monthly":
        df_clean = df_clean.set_index('date').resample('ME').mean().reset_index()
    elif time_res == "Yearly":
        df_clean = df_clean.set_index('date').resample('YE').mean().reset_index()

    return selected_product, df_clean
