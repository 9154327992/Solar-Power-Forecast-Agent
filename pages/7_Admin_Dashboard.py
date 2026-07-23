import streamlit as st
import requests
import pandas as pd
from pathlib import Path

# ==========================================================
# Configuration
# ==========================================================

API_URL = "https://solar-power-forecast-agent.onrender.com"

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="⚙️",
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

st.title("⚙️ Admin Dashboard")

st.write(
    "Monitor the Solar Power Forecast Agent and manage backend resources."
)

st.divider()

# ==========================================================
# System Health
# ==========================================================

st.subheader("🟢 System Health")

col1, col2, col3 = st.columns(3)

try:

    health = requests.get(
        f"{API_URL}/health",
        timeout=10
    ).json()

    api_status = "Online"

except Exception:

    api_status = "Offline"

with col1:
    st.metric("Backend API", api_status)

with col2:
    st.metric("ML Model", "Loaded")

with col3:
    st.metric("Database", "Connected")

st.divider()

# ==========================================================
# Model Information
# ==========================================================

st.subheader("🧠 Model Information")

try:

    model = requests.get(
        f"{API_URL}/model-info",
        timeout=10
    ).json()

    st.json(model)

except:

    st.info("Model information unavailable.")

st.divider()

# ==========================================================
# Database Statistics
# ==========================================================

st.subheader("🗄 Database Statistics")

try:

    stats = requests.get(
        f"{API_URL}/database-stats",
        timeout=10
    ).json()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Predictions",
            stats["predictions"]
        )

    with c2:
        st.metric(
            "Users",
            stats["users"]
        )

    with c3:
        st.metric(
            "Reports",
            stats["reports"]
        )

except:

    st.warning("Database statistics unavailable.")

st.divider()

# ==========================================================
# Dataset Upload
# ==========================================================

st.subheader("📂 Upload Dataset")

dataset = st.file_uploader(
    "Upload CSV Dataset",
    type=["csv"]
)

if dataset is not None:

    if st.button(
        "Upload Dataset",
        use_container_width=True
    ):

        try:

            files = {
                "file": (
                    dataset.name,
                    dataset.getvalue(),
                    "text/csv"
                )
            }

            response = requests.post(
                f"{API_URL}/upload-dataset",
                files=files,
                timeout=60
            )

            response.raise_for_status()

            st.success("Dataset uploaded successfully.")

        except Exception as e:

            st.error(e)

st.divider()

# ==========================================================
# Retrain Model
# ==========================================================

st.subheader("🔄 Retrain Model")

if st.button(
    "Retrain Machine Learning Model",
    use_container_width=True
):

    with st.spinner("Training model..."):

        try:

            response = requests.post(
                f"{API_URL}/retrain",
                timeout=300
            )

            response.raise_for_status()

            result = response.json()

            st.success(result["message"])

        except Exception as e:

            st.error(e)

st.divider()

# ==========================================================
# Download Database Backup
# ==========================================================

st.subheader("💾 Database Backup")

if st.button(
    "Generate Backup",
    use_container_width=True
):

    try:

        response = requests.get(
            f"{API_URL}/backup",
            timeout=120
        )

        response.raise_for_status()

        st.download_button(
            "⬇ Download Backup",
            response.content,
            "solar_backup.db",
            use_container_width=True
        )

    except Exception as e:

        st.error(e)

st.divider()

# ==========================================================
# System Logs
# ==========================================================

st.subheader("📜 System Logs")

try:

    logs = requests.get(
        f"{API_URL}/logs",
        timeout=20
    ).json()

    log_df = pd.DataFrame(logs)

    st.dataframe(
        log_df,
        use_container_width=True,
        hide_index=True
    )

except:

    st.info("No logs available.")

st.divider()

# ==========================================================
# API Endpoints
# ==========================================================

st.subheader("🌐 API Endpoints")

st.code("""
GET     /health
POST    /forecast
GET     /history
DELETE  /history
POST    /ai-assistant
GET     /model-info
POST    /upload-dataset
POST    /retrain
GET     /database-stats
GET     /backup
GET     /logs
""")

st.divider()

# ==========================================================
# Footer
# ==========================================================

st.caption(
    "Solar Power Forecast Agent • Admin Dashboard"
)