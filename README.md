# 🌾 CEPEA Dashboard - Agricultural Input Price Forecast

Interactive dashboard that automatically collects, stores, and forecasts agricultural input prices (live cattle, rice, coffee, and the dollar) based on data provided by CEPEA (Center for Advanced Studies in Applied Economics).

## 🛠️ How to Use

✅ Access the dashboard:
https://dashboard-cepea-app.onrender.com

(ℹ️ It may take a while to load, as I'm using Render's free plan.)

## 📊 The system performs:

Automated data collection directly from the CEPEA website.
Conversion and insertion into a PostgreSQL database.
Predictive modeling with XGBoost.
Historical data visualization and forecasting via Streamlit.
Fully automated daily updates with GitHub Actions. 🚀 Technologies Used

* Python 3.10
* Streamlit – Interactive interface
* PostgreSQL – Data storage
* Selenium / Requests – Web scraping of CEPEA files
* LibreOffice (CLI) – Conversion from .xls to .xlsx
* Pandas / NumPy – Data manipulation
* XGBoost / Scikit-learn – Predictive modeling
* Matplotlib – Graph visualization
* Docker – Application containerization
* Render.com – Webapp + database deployment
* GitHub Actions – Daily update automation

