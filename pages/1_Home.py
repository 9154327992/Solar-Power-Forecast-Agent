import streamlit as st
from pathlib import Path

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Home | Solar Power Forecast Agent",
    page_icon="☀️",
    layout="wide"
)

# ============================================================
# Load Custom CSS
# ============================================================

css_file = Path("assets/style.css")

if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ============================================================
# Header
# ============================================================

col1, col2 = st.columns([1, 5])

with col1:
    logo = Path("assets/logo.png")
    if logo.exists():
        st.image(str(logo), width=100)

with col2:
    st.title("☀ Solar Power Forecast Agent")
    st.write(
        "AI-powered Solar Energy Forecasting and Intelligent Energy Recommendation System."
    )

st.divider()

# ============================================================
# Banner
# ============================================================

banner = Path("assets/banner.jpg")

if banner.exists():
    st.image(str(banner), use_container_width=True)

st.divider()

# ============================================================
# Dashboard Cards
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("ML Model", "XGBoost")

with c2:
    st.metric("Prediction Type", "Regression")

with c3:
    st.metric("Weather Inputs", "9")

with c4:
    st.metric("Status", "Ready")

st.divider()

# ============================================================
# About Project
# ============================================================

st.header("📌 About the Project")

st.write("""
The **Solar Power Forecast Agent** is an AI-powered application that predicts
solar energy generation using weather parameters.

The system combines Machine Learning, weather analytics,
and intelligent recommendations to help users optimize
solar energy usage.
""")

st.divider()

# ============================================================
# Features
# ============================================================

st.header("🚀 Features")

left, right = st.columns(2)

with left:

    st.success("✔ Solar Power Forecast")

    st.success("✔ Live Weather")

    st.success("✔ AI Energy Assistant")

    st.success("✔ Prediction History")

with right:

    st.success("✔ Analytics Dashboard")

    st.success("✔ Report Generation")

    st.success("✔ Admin Dashboard")

    st.success("✔ Custom Settings")

st.divider()

# ============================================================
# Technology Stack
# ============================================================

st.header("🛠 Technology Stack")

tech1, tech2, tech3 = st.columns(3)

with tech1:

    st.info("""
    **Frontend**

    • Streamlit

    • HTML

    • CSS
    """)

with tech2:

    st.info("""
    **Backend**

    • Python

    • FastAPI

    • SQLite
    """)

with tech3:

    st.info("""
    **Machine Learning**

    • XGBoost

    • Scikit-Learn

    • Pandas
    """)

st.divider()

# ============================================================
# Workflow
# ============================================================

st.header("⚙ System Workflow")

st.code("""
Weather Data
      │
      ▼
Data Preprocessing
      │
      ▼
Feature Engineering
      │
      ▼
XGBoost Model
      │
      ▼
Solar Power Prediction
      │
      ▼
AI Recommendation Engine
      │
      ▼
Analytics Dashboard
""")

st.divider()

# ============================================================
# Navigation Guide
# ============================================================

st.header("📂 Application Pages")

pages = [
    "🏠 Home",
    "☀ Solar Forecast",
    "🌦 Live Weather",
    "🤖 AI Energy Assistant",
    "📜 Prediction History",
    "📊 Analytics Dashboard",
    "🛠 Admin Dashboard",
    "⚙ Settings"
]

for page in pages:
    st.write("•", page)

st.info("Use the left sidebar to navigate between pages.")

st.divider()

# ============================================================
# Developer
# ============================================================

st.header("👨‍💻 Developer")

st.write("""
Developed as an end-to-end Machine Learning project using:

- Python
- Streamlit
- FastAPI
- XGBoost
- SQLite
- Artificial Intelligence
""")

st.divider()

# ============================================================
# Footer
# ============================================================

st.markdown(
"""
<div style="text-align:center;">
<h3>☀ Solar Power Forecast Agent</h3>
<p>
Machine Learning • Artificial Intelligence • FastAPI • Streamlit
</p>
</div>
""",
unsafe_allow_html=True
)

st.caption(
    "© 2026 Solar Power Forecast Agent | All Rights Reserved"
)