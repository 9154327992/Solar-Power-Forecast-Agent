# ============================================================
# train_model.py
# Solar Power Forecast Model Training
# ============================================================

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from xgboost import XGBRegressor


# ============================================================
# Paths
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "solar_power.csv"
)

MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")


# ============================================================
# Load Dataset
# ============================================================

def load_dataset():

    dataset = pd.read_csv(DATASET_PATH)

    dataset["Date-Hour(NMT)"] = pd.to_datetime(
        dataset["Date-Hour(NMT)"]
    )

    return dataset


# ============================================================
# Prepare Features
# ============================================================

def prepare_features(dataset):

    X = dataset[
        [
            "WindSpeed",
            "Sunshine",
            "AirPressure",
            "Radiation",
            "AirTemperature",
            "RelativeAirHumidity",
        ]
    ].copy()

    X["Hour"] = dataset["Date-Hour(NMT)"].dt.hour
    X["Day"] = dataset["Date-Hour(NMT)"].dt.day
    X["Month"] = dataset["Date-Hour(NMT)"].dt.month

    y = dataset["SystemProduction"]

    return X, y


# ============================================================
# Train Model
# ============================================================

def train():

    dataset = load_dataset()

    X, y = prepare_features(dataset)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)

    X_test_scaled = scaler.transform(X_test)

    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )

    model.fit(X_train_scaled, y_train)

    predictions = model.predict(X_test_scaled)

    mae = mean_absolute_error(y_test, predictions)

    rmse = mean_squared_error(
        y_test,
        predictions,
        squared=False,
    )

    r2 = r2_score(
        y_test,
        predictions,
    )

    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    joblib.dump(scaler, SCALER_PATH)

    print("=" * 50)
    print("Training Complete")
    print("=" * 50)
    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R²   : {r2:.4f}")
    print("=" * 50)
    print(f"Model saved  : {MODEL_PATH}")
    print(f"Scaler saved : {SCALER_PATH}")


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    train()