import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ==========================================================
# Configuration
# ==========================================================

API_URL = "https://solar-power-forecast-agent.onrender.com"

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# Load CSS
# ==========================================================

css = Path("assets/style.css")

if css.exists():
    with open(css) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ==========================================================
# Header
# ==========================================================

st.title("📊 Analytics Dashboard")

st.write(
    "Visual insights into historical solar power predictions."
)

st.divider()

# ==========================================================
# Load Prediction History
# ==========================================================

try:

    response = requests.get(
        f"{API_URL}/history",
        timeout=20
    )

    response.raise_for_status()

    history = pd.DataFrame(response.json())

except Exception as e:

    st.error(e)

    st.stop()

if history.empty:

    st.warning("No prediction history available.")

    st.stop()

# ==========================================================
# Data Preparation
# ==========================================================

history["predicted_power_kw"] = history["predicted_power"] / 1000

history.index = range(1, len(history)+1)

# ==========================================================
# KPI Cards
# ==========================================================

st.subheader("📈 Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Total Predictions",
        len(history)
    )

with c2:

    st.metric(
        "Average Power",
        f"{history['predicted_power_kw'].mean():.2f} kW"
    )

with c3:

    st.metric(
        "Maximum Power",
        f"{history['predicted_power_kw'].max():.2f} kW"
    )

with c4:

    st.metric(
        "Minimum Power",
        f"{history['predicted_power_kw'].min():.2f} kW"
    )

st.divider()

# ==========================================================
# Prediction Trend
# ==========================================================

st.subheader("📈 Prediction Trend")

trend = px.line(

    history,

    x=history.index,

    y="predicted_power_kw",

    markers=True,

    title="Solar Power Prediction Trend"

)

trend.update_layout(

    xaxis_title="Prediction Number",

    yaxis_title="Power (kW)"

)

st.plotly_chart(

    trend,

    use_container_width=True

)

# ==========================================================
# Generation Distribution
# ==========================================================

st.subheader("☀ Generation Level Distribution")

distribution = px.pie(

    history,

    names="generation_level",

    title="Generation Level Distribution"

)

st.plotly_chart(

    distribution,

    use_container_width=True

)

# ==========================================================
# Histogram
# ==========================================================

st.subheader("📉 Power Distribution")

histogram = px.histogram(

    history,

    x="predicted_power_kw",

    nbins=20,

    title="Distribution of Predicted Power"

)

st.plotly_chart(

    histogram,

    use_container_width=True

)

# ==========================================================
# Box Plot
# ==========================================================

st.subheader("📦 Prediction Spread")

box = px.box(

    history,

    y="predicted_power_kw",

    points="all",

    title="Predicted Power Spread"

)

st.plotly_chart(

    box,

    use_container_width=True

)

# ==========================================================
# Daily Average
# ==========================================================

if "date" in history.columns:

    st.subheader("📅 Daily Average Generation")

    daily = history.groupby(

        "date",

        as_index=False

    )["predicted_power_kw"].mean()

    chart = px.bar(

        daily,

        x="date",

        y="predicted_power_kw",

        title="Average Daily Solar Power"

    )

    st.plotly_chart(

        chart,

        use_container_width=True

    )

# ==========================================================
# Generation Level Counts
# ==========================================================

st.subheader("📊 Generation Level Count")

count = history["generation_level"].value_counts()

fig = go.Figure(

    data=[

        go.Bar(

            x=count.index,

            y=count.values

        )

    ]

)

fig.update_layout(

    title="Generation Level Frequency",

    xaxis_title="Generation Level",

    yaxis_title="Count"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ==========================================================
# Data Table
# ==========================================================

st.subheader("📋 Prediction Dataset")

st.dataframe(

    history,

    use_container_width=True,

    hide_index=True

)

# ==========================================================
# Export Analytics
# ==========================================================

st.divider()

st.download_button(

    "⬇ Download Analytics Data",

    history.to_csv(index=False),

    "analytics.csv",

    "text/csv",

    use_container_width=True

)

# ==========================================================
# Footer
# ==========================================================

st.caption(

    "Solar Power Forecast Agent • Analytics Dashboard"

)