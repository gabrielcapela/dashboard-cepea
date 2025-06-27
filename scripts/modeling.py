import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
import joblib

############################## DATA PREPARATION ##############################

conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "../data/cepea.db"))
df = pd.read_sql("SELECT * FROM prices ORDER BY date", conn)
conn.close()

numeric_cols = ['dollar', 'fattened_cattle', 'rice', 'coffee']
for col in numeric_cols:
    df[col] = (
        df[col].astype(str)
        .replace('None', np.nan)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .astype(float)
    )

df['date'] = pd.to_datetime(df['date'])

prepared_dfs = {}
targets = ['fattened_cattle', 'rice', 'coffee']
for target in targets:
    df_target = df[['date', 'dollar', target]].copy()
    df_target.columns = ['ds', 'dollar', 'y']
    df_target.dropna(inplace=True)
    for lag in [1, 2, 3]:
        df_target[f'y_lag_{lag}'] = df_target['y'].shift(lag)
    df_target['day_of_week'] = df_target['ds'].dt.dayofweek
    df_target['month'] = df_target['ds'].dt.month
    df_target.dropna(inplace=True)
    prepared_dfs[target] = df_target

############################## MODELING AND SAVING ##############################

features = ['dollar', 'y_lag_1', 'y_lag_2', 'y_lag_3', 'day_of_week', 'month']
xgb_results = {}

os.makedirs("models", exist_ok=True)
os.makedirs("metrics", exist_ok=True)

for name, df in prepared_dfs.items():
    print(f"\n🔁 Starting pipeline for: {name}")
    df = df.sort_values('ds')
    n = len(df)
    train_end = int(n * 0.7)
    val_end = int(n * 0.9)
    df_train = df.iloc[:train_end]
    df_val = df.iloc[train_end:val_end]
    df_test = df.iloc[val_end:]

    X_train, y_train = df_train[features], df_train['y']
    X_val, y_val = df_val[features], df_val['y']
    X_test, y_test = df_test[features], df_test['y']

    base_model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    base_model.fit(X_train, y_train)
    mape_val = mean_absolute_percentage_error(y_val, base_model.predict(X_val))

    param_grid = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.05, 0.1],
        'max_depth': [3, 4, 5],
        'subsample': [0.7, 0.8, 1.0],
        'colsample_bytree': [0.7, 0.8, 1.0]
    }

    tscv = TimeSeriesSplit(n_splits=3)
    random_search = RandomizedSearchCV(
        estimator=XGBRegressor(random_state=42),
        param_distributions=param_grid,
        n_iter=20,
        scoring='neg_mean_absolute_percentage_error',
        cv=tscv,
        verbose=0,
        n_jobs=-1,
        random_state=42
    )
    random_search.fit(X_train, y_train)
    best_model = random_search.best_estimator_

    mape_val_tuned = mean_absolute_percentage_error(y_val, best_model.predict(X_val))
    mape_test = mean_absolute_percentage_error(y_test, best_model.predict(X_test))

    final_model_all = XGBRegressor(**best_model.get_params())
    final_model_all.fit(df[features], df['y'])
    joblib.dump(final_model_all, f'models/{name}_xgb_model.pkl')

    metrics_data = {
        "mape_val_initial": round(mape_val, 4),
        "mape_val_tuned": round(mape_val_tuned, 4),
        "mape_test": round(mape_test, 4)
    }
    with open(f"metrics/{name}_metrics.json", "w") as f:
        json.dump(metrics_data, f, indent=4)

    # Save forecast data
    df_plot = df.copy()
    recent_df = df_plot.tail(20)[['ds', 'y']].copy()
    future_dates = pd.date_range(start=df_plot['ds'].max() + pd.Timedelta(days=1), periods=5)
    last_ys = df_plot['y'].tail(3).tolist()[::-1]
    dollar_value = df_plot['dollar'].iloc[-1]

    future_predictions = []
    for date in future_dates:
        X_input = pd.DataFrame([{
            'dollar': dollar_value,
            'y_lag_1': last_ys[0],
            'y_lag_2': last_ys[1],
            'y_lag_3': last_ys[2],
            'day_of_week': date.dayofweek,
            'month': date.month
        }])
        y_next = final_model_all.predict(X_input)[0]
        future_predictions.append((date, y_next))
        last_ys = [y_next] + last_ys[:2]

    future_df = pd.DataFrame(future_predictions, columns=['ds', 'y'])
    plot_df = pd.concat([recent_df, future_df], ignore_index=True)
    plot_df.to_csv(f"data/plot_data/{name}_forecast.csv", index=False)

    #print(f"✅ {name} done. Metrics and forecast saved.")
