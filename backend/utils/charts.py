# ============================================================
# charts.py
# Visualization Utilities
# ============================================================

import pandas as pd
import plotly.express as px
import streamlit as st


class Charts:

    @staticmethod
    def prediction_history(data):

        if not data:
            st.info("No prediction history available.")
            return

        df = pd.DataFrame(data)

        fig = px.line(
            df,
            x="timestamp",
            y="prediction",
            title="Solar Power Prediction History",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def weather_chart(weather):

        df = pd.DataFrame({
            "Feature": [
                "Temperature",
                "Humidity",
                "Pressure",
                "Wind Speed",
                "Cloud Cover"
            ],
            "Value": [
                weather["temperature"],
                weather["humidity"],
                weather["pressure"],
                weather["wind_speed"],
                weather["cloud_cover"]
            ]
        })

        fig = px.bar(
            df,
            x="Feature",
            y="Value",
            title="Current Weather"
        )

        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def efficiency_gauge(efficiency):

        fig = px.pie(
            values=[efficiency, 100 - efficiency],
            names=["Efficiency", "Remaining"],
            hole=0.7,
            title="Solar Efficiency"
        )

        st.plotly_chart(fig, use_container_width=True)


charts = Charts()