# ============================================================
# preprocessing.py
# Dataset Preprocessing
# ============================================================

import pandas as pd


class DataPreprocessor:
    """
    Preprocesses the historical solar dataset before training.
    """

    def load_dataset(self, filepath):
        """
        Load the dataset.
        """
        return pd.read_csv(filepath)

    def preprocess(self, dataframe):
        """
        Clean and prepare the dataset.
        """

        df = dataframe.copy()

        # Convert date column
        df["Date-Hour(NMT)"] = pd.to_datetime(df["Date-Hour(NMT)"])

        # Create time features
        df["Hour"] = df["Date-Hour(NMT)"].dt.hour
        df["Day"] = df["Date-Hour(NMT)"].dt.day
        df["Month"] = df["Date-Hour(NMT)"].dt.month

        # Remove missing values
        df.dropna(inplace=True)

        # Remove duplicate rows
        df.drop_duplicates(inplace=True)

        return df

    def get_features_target(self, dataframe):
        """
        Split dataset into features and target.
        """

        features = [

            "WindSpeed",

            "Sunshine",

            "AirPressure",

            "Radiation",

            "AirTemperature",

            "RelativeAirHumidity",

            "Hour",

            "Day",

            "Month"

        ]

        X = dataframe[features]
        y = dataframe["SystemProduction"]

        return X, y


# Global instance
preprocessor = DataPreprocessor()