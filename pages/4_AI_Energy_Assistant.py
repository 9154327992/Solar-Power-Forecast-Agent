import streamlit as st
import requests
from pathlib import Path

# ==========================================================
# Configuration
# ==========================================================

API_URL = "https://solar-power-forecast-agent.onrender.com"

st.set_page_config(
    page_title="AI Energy Assistant",
    page_icon="🤖",
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
# Session State
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# Header
# ==========================================================

st.title("🤖 AI Energy Assistant")

st.write(
    "Ask questions about solar power, weather, battery usage, and energy optimization."
)

st.divider()

# ==========================================================
# Quick Questions
# ==========================================================

st.subheader("⚡ Quick Questions")

c1, c2 = st.columns(2)

with c1:

    if st.button("Will solar generation be high today?"):
        st.session_state.prompt = "Will solar generation be high today?"

    if st.button("Should I charge my battery now?"):
        st.session_state.prompt = "Should I charge my battery now?"

    if st.button("Can I run heavy appliances now?"):
        st.session_state.prompt = "Can I run heavy appliances now?"

with c2:

    if st.button("Explain today's forecast"):
        st.session_state.prompt = "Explain today's forecast."

    if st.button("Give energy saving tips"):
        st.session_state.prompt = "Give me energy saving tips."

    if st.button("Generate a daily report"):
        st.session_state.prompt = "Generate a daily solar energy report."

st.divider()

# ==========================================================
# Chat Interface
# ==========================================================

st.subheader("💬 Chat")

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

default_prompt = st.session_state.get("prompt", "")

user_prompt = st.chat_input(
    "Ask anything about solar energy..."
)

if not user_prompt and default_prompt:
    user_prompt = default_prompt
    st.session_state.prompt = ""

# ==========================================================
# AI Processing
# ==========================================================

if user_prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = requests.post(

                    f"{API_URL}/ai-assistant",

                    json={
                        "question": user_prompt
                    },

                    timeout=30

                )

                response.raise_for_status()

                answer = response.json()["response"]

            except Exception:

                # Fallback responses

                prompt = user_prompt.lower()

                if "battery" in prompt:

                    answer = (
                        "Charge the battery during high solar generation "
                        "hours between 10 AM and 3 PM."
                    )

                elif "forecast" in prompt:

                    answer = (
                        "Solar generation depends mainly on solar radiation, "
                        "sunshine duration, cloud cover, and temperature."
                    )

                elif "heavy" in prompt:

                    answer = (
                        "Operate washing machines, pumps, or EV charging "
                        "during peak solar generation hours."
                    )

                elif "saving" in prompt:

                    answer = (
                        "Use appliances during daylight, clean solar panels "
                        "regularly, and avoid unnecessary standby loads."
                    )

                elif "report" in prompt:

                    answer = (
                        "Daily Report\n\n"
                        "- Monitor weather.\n"
                        "- Forecast solar generation.\n"
                        "- Charge batteries during peak sunlight.\n"
                        "- Shift heavy loads to midday."
                    )

                else:

                    answer = (
                        "I'm your Solar Energy Assistant. "
                        "Ask me about forecasting, battery usage, "
                        "maintenance, weather, or energy optimization."
                    )

        st.markdown(answer)

    st.session_state.messages.append(

        {
            "role": "assistant",
            "content": answer
        }

    )

st.divider()

# ==========================================================
# AI Capabilities
# ==========================================================

st.subheader("🧠 AI Capabilities")

col1, col2 = st.columns(2)

with col1:

    st.success("✔ Explain Solar Forecast")

    st.success("✔ Battery Recommendations")

    st.success("✔ Appliance Scheduling")

    st.success("✔ Weather Interpretation")

with col2:

    st.success("✔ Energy Saving Tips")

    st.success("✔ Maintenance Advice")

    st.success("✔ Daily Report")

    st.success("✔ Smart Recommendations")

st.divider()

# ==========================================================
# Footer
# ==========================================================

st.caption(
    "Powered by Artificial Intelligence • Solar Power Forecast Agent"
)