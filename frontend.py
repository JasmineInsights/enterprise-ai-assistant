import streamlit as st
import requests

API_URL = "https://enterprise-ai-assistant-43az.onrender.com"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM STYLE ----------------
st.markdown("""
<style>
.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
}

.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.title("📁 Document Hub")

    uploaded_file = st.file_uploader(
        "Upload Document",
        type=["pdf", "docx", "pptx"]
    )

    if uploaded_file:

        if st.button("Upload"):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    uploaded_file.type
                )
            }

            try:

                res = requests.post(
                    f"{API_URL}/upload",
                    files=files,
                    timeout=60
                )

                if res.status_code == 200:

                    data = res.json()

                    st.success("Uploaded Successfully 🚀")

                    st.json({
                        "filename": data["filename"],
                        "chunks_stored": data["chunks_stored"]
                    })

                else:
                    st.error("Upload failed. Please try again.")

            except Exception:
                st.error("Upload failed. Please try again.")

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;color:#38bdf8;'>
        🤖 Enterprise AI Assistant
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center;color:#94a3b8;'>
        Chat with your documents using AI
    </p>
    """,
    unsafe_allow_html=True
)

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- QUESTION INPUT ----------------
question = st.text_input(
    "Ask anything from your documents..."
)

if st.button("🚀 Ask") and question:

    try:

        res = requests.post(
            f"{API_URL}/chat",
            json={"question": question},
            timeout=120
        )

        if res.status_code == 200:

            data = res.json()

            st.session_state.chat_history.append(
                {
                    "q": question,
                    "a": data.get("answer", ""),
                    "s": data.get("sources", [])
                }
            )

        else:
            st.error("Unable to get response from AI Assistant.")

    except Exception:
        st.error("Unable to get response from AI Assistant.")

# ---------------- CHAT DISPLAY ----------------
for chat in reversed(st.session_state.chat_history):

    with st.chat_message("user"):
        st.write(chat["q"])

    with st.chat_message("assistant"):
        st.write(chat["a"])

        if chat["s"]:
            st.caption(
                "📌 Sources: " +
                ", ".join(chat["s"])
            )