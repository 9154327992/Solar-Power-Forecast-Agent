# ============================================================
# feature_engineering.py
# Feature Engineering
# ============================================================

import pandas as pd


class FeatureEngineer:
    """
    Creates additional features for solar power prediction.
    """

    def add_time_features(self, dataframe):
        """
        Extract time-related features from Date-Hour(NMT).
        """

        df = dataframe.copy()

        if "Date-Hour(NMT)" in df.columns:

            df["Date-Hour(NMT)"] = pd.to_datetime(df["Date-Hour(NMT)"])

            df["Hour"] = df["Date-Hour(NMT)"].dt.hour
            df["Day"] = df["Date-Hour(NMT)"].dt.day
            df["Month"] = df["Date-Hour(NMT)"].dt.month
            df["DayOfWeek"] = df["Date-Hour(NMT)"].dt.dayofweek

        return df

    def add_weather_features(self, dataframe):
        """
        Create derived weather features.
        """

        df = dataframe.copy()

        if (
            "AirTemperature" in df.columns and
            "RelativeAirHumidity" in df.columns
        ):

            df["TempHumidityIndex"] = (
                df["AirTemperature"] *
                df["RelativeAirHumidity"] / 100
            )

        if (
            "Radiation" in df.columns and
            "Sunshine" in df.columns
        ):

            df["RadiationPerSunshine"] = (
                df["Radiation"] /
                (df["Sunshine"] + 1)
            )

        return df

    def build_features(self, dataframe):
        """
        Complete feature engineering pipeline.
        """

        df = self.add_time_features(dataframe)
        df = self.add_weather_features(df)

        return df


# Global instance
feature_engineer = FeatureEngineer()