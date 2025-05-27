import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Page title
st.title("CEPEA Price Dashboard")

# Connect to the SQLite database
conn = sqlite3.connect("data/cepea.db")

# Load all records from the 'prices' table
df = pd.read_sql("SELECT * FROM prices ORDER BY date", conn)

# Close the database connection
conn.close()

# Commodity selector
product = st.selectbox("Select a commodity", ['fattened_cattle', 'rice', 'coffee', 'dollar'])

# Convert 'date' to datetime and product column to numeric
df['date'] = pd.to_datetime(df['date']).dt.date
df[product] = pd.to_numeric(
    df[product].str.replace('.', '', regex=False).str.replace(',', '.', regex=False),
    errors='coerce'
)


# Filter and clean the data for plotting
data_to_plot = df[['date', product]].dropna()

# Create the line plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data_to_plot['date'], data_to_plot[product], marker='o')

# Customize the plot
ax.set_title(f'{product.replace("_", " ").title()} Price Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)

# Optional: display the filtered data table
st.caption("Price history for selected commodity")
st.dataframe(data_to_plot)
