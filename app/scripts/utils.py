import pandas as pd
import streamlit as st

def get_clean_data(df):
    """
    Display commodity and time resolution selectors, return cleaned and optionally resampled data.

    Args:
        df (pd.DataFrame): Original DataFrame with 'date' and commodity columns.

    Returns:
        product (str): Selected commodity
        data_to_plot (pd.DataFrame): DataFrame with date and selected product, possibly resampled
    """
    # Commodity selector
    product = st.selectbox("Select a commodity", ['fattened_cattle', 'rice', 'coffee', 'dollar'])

    # Time resolution selector
    time_res = st.radio("Select time resolution", ["Daily", "Monthly", "Yearly"], horizontal=True)

    # Convert date and clean price column
    df['date'] = pd.to_datetime(df['date'])
    df[product] = pd.to_numeric(
        df[product].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False),
        errors='coerce'
    )

    df_clean = df[['date', product]].dropna()

    # Resample based on time resolution
    if time_res == "Monthly":
        df_clean = (
            df_clean
            .set_index('date')
            .resample('M')
            .mean()
            .reset_index()
        )
    elif time_res == "Yearly":
        df_clean = (
            df_clean
            .set_index('date')
            .resample('Y')
            .mean()
            .reset_index()
        )

    return product, df_clean
