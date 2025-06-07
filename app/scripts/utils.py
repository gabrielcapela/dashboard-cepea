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
                st.image(image_path, width=300)
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
        # st.session_state.start_date = None    # resets the start and end dates of the graph
        # st.session_state.end_date = None      # resets the start and end dates of the graph
        st.session_state.time_res = time_res
    ##########################################



    # Clean and prepare data according to selected parameters
    df['date'] = pd.to_datetime(df['date'])
    df[selected_product] = pd.to_numeric(
        df[selected_product].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False),
        errors='coerce'
    )

    df_clean = df[['date', selected_product]].dropna()

    # if time_res == "Monthly":
    #     df_clean = df_clean.set_index('date').resample('M').mean()
    #     df_clean.index = df_clean.index.to_period('M').to_timestamp(how='start')
    #     df_clean = df_clean.reset_index()
    # elif time_res == "Yearly":
    #     df_clean = df_clean.set_index('date').resample('Y').mean()
    #     df_clean.index = df_clean.index.to_period('Y').to_timestamp(how='start')
    #     df_clean = df_clean.reset_index()

    if time_res == "Monthly":
        df_clean = df_clean.set_index('date').resample('MS').mean().reset_index()
    elif time_res == "Yearly":
        df_clean = df_clean.set_index('date').resample('YS').mean().reset_index()



    return  df_clean, selected_product, time_res
