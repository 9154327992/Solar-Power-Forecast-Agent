import streamlit as st
import requests
from pathlib import Path
import streamlit.components.v1 as components


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

    with open(css, encoding="utf-8") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


# ==========================================================
# Session State
# ==========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "prompt" not in st.session_state:

    st.session_state.prompt = ""


# ==========================================================
# Header
# ==========================================================

st.title("🤖 AI Energy Assistant")

st.write(
    "Ask questions about solar power, weather, "
    "battery usage, appliances, maintenance, "
    "and energy optimization."
)

st.divider()


# ==========================================================
# Quick Questions
# ==========================================================

st.subheader("⚡ Quick Questions")

st.caption(
    "These are shortcuts. You can also type any "
    "solar or energy question below."
)


col1, col2 = st.columns(2)


with col1:

    if st.button(
        "Will solar generation be high today?",
        use_container_width=True
    ):

        st.session_state.prompt = (
            "Will solar generation be high today?"
        )

        st.session_state.auto_scroll = True


    if st.button(
        "Should I charge my battery now?",
        use_container_width=True
    ):

        st.session_state.prompt = (
            "Should I charge my battery now?"
        )

        st.session_state.auto_scroll = True


    if st.button(
        "Can I run heavy appliances now?",
        use_container_width=True
    ):

        st.session_state.prompt = (
            "Can I run heavy appliances now?"
        )

        st.session_state.auto_scroll = True


with col2:

    if st.button(
        "Explain today's forecast",
        use_container_width=True
    ):

        st.session_state.prompt = (
            "Explain today's forecast."
        )

        st.session_state.auto_scroll = True


    if st.button(
        "Give energy saving tips",
        use_container_width=True
    ):

        st.session_state.prompt = (
            "Give me energy saving tips."
        )

        st.session_state.auto_scroll = True


    if st.button(
        "Generate a daily report",
        use_container_width=True
    ):

        st.session_state.prompt = (
            "Generate a daily solar energy report."
        )

        st.session_state.auto_scroll = True


st.divider()


# ==========================================================
# Chat
# ==========================================================

st.subheader("💬 Chat")


# ----------------------------------------------------------
# Display Previous Messages
# ----------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==========================================================
# Chat Input
# ==========================================================

user_prompt = st.chat_input(
    "Ask anything about solar energy..."
)


# ==========================================================
# Quick Question Handler
# ==========================================================

if not user_prompt:

    if st.session_state.prompt:

        user_prompt = st.session_state.prompt

        st.session_state.prompt = ""


# ==========================================================
# Process Question
# ==========================================================

if user_prompt:

    # ------------------------------------------------------
    # Store User Message
    # ------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )


    # ------------------------------------------------------
    # Display User Message
    # ------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(user_prompt)


    # ------------------------------------------------------
    # Assistant Response
    # ------------------------------------------------------

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


                result = response.json()


                answer = result.get(
                    "response",
                    "I couldn't generate a response."
                )


            except requests.exceptions.Timeout:

                answer = (
                    "⏳ The backend took too long to respond.\n\n"
                    "Please try your question again."
                )


            except requests.exceptions.ConnectionError:

                answer = (
                    "🔌 I couldn't connect to the backend.\n\n"
                    "Please check whether the backend service "
                    "is currently running."
                )


            except Exception as error:

                answer = (
                    "⚠️ I couldn't process that request right now.\n\n"
                    f"Error: {str(error)}"
                )


        st.markdown(answer)


    # ------------------------------------------------------
    # Store Assistant Message
    # ------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # ------------------------------------------------------
    # Auto Scroll
    # ------------------------------------------------------

    st.session_state.auto_scroll = True


# ==========================================================
# Auto Scroll To Latest Answer
# ==========================================================

if st.session_state.get(
    "auto_scroll",
    False
):

    components.html(
        """
        <script>

        function scrollToLatestAnswer() {

            try {

                const parentDocument =
                    window.parent.document;

                const messages =
                    parentDocument.querySelectorAll(
                        '[data-testid="stChatMessage"]'
                    );

                if (messages.length > 0) {

                    const lastMessage =
                        messages[messages.length - 1];

                    lastMessage.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });
                }

            } catch (error) {

                console.log(
                    "Auto-scroll error:",
                    error
                );
            }
        }


        setTimeout(
            scrollToLatestAnswer,
            100
        );

        setTimeout(
            scrollToLatestAnswer,
            500
        );

        setTimeout(
            scrollToLatestAnswer,
            1000
        );

        </script>
        """,
        height=0
    )

    st.session_state.auto_scroll = False


# ==========================================================
# AI Capabilities
# ==========================================================

st.divider()

st.subheader("🧠 AI Capabilities")


col1, col2 = st.columns(2)


with col1:

    st.success(
        "✔ Solar Forecast Explanation"
    )

    st.success(
        "✔ Battery Recommendations"
    )

    st.success(
        "✔ Appliance Scheduling"
    )

    st.success(
        "✔ Weather Interpretation"
    )


with col2:

    st.success(
        "✔ Energy Saving Tips"
    )

    st.success(
        "✔ Solar Panel Maintenance"
    )

    st.success(
        "✔ XGBoost / ML Explanation"
    )

    st.success(
        "✔ Daily Solar Reports"
    )


st.divider()


# ==========================================================
# Footer
# ==========================================================

st.caption(
    "Powered by Artificial Intelligence • "
    "Solar Power Forecast Agent"
)
