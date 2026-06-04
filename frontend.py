import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM STYLE ----------------
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: white;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
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

            res = requests.post(
                f"{API_URL}/upload",
                files=files
            )

            st.success("Uploaded Successfully 🚀")
            st.json(res.json())

# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align: center; color: #38bdf8;'>🤖 Enterprise AI Assistant</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: #94a3b8;'>Chat with your documents using AI</p>",
    unsafe_allow_html=True
)

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- INPUT BOX ----------------
question = st.text_input("Ask anything from your documents...")

col1, col2 = st.columns([1, 5])

with col1:
    ask = st.button("🚀 Ask")

if ask and question:

    res = requests.post(
        f"{API_URL}/chat",
        json={"question": question}
    )

    data = res.json()

    st.session_state.chat_history.append(
        {
            "q": question,
            "a": data["answer"],
            "s": data["sources"]
        }
    )

# ---------------- CHAT DISPLAY ----------------
for chat in reversed(st.session_state.chat_history):

    st.markdown(
        f"""
        <div style="
            background-color:#1e293b;
            padding:16px;
            border-radius:12px;
            margin-bottom:12px;
            border:1px solid #334155;
            color:#e2e8f0;
        ">

        <div style="margin-bottom:10px;">
            <b style="color:#38bdf8;">🧑 You:</b><br>
            {chat['q']}
        </div>

        <div style="margin-bottom:10px;">
            <b style="color:#22c55e;">🤖 AI:</b><br>
            {chat['a']}
        </div>

        <div style="
            background-color:#0f172a;
            padding:10px;
            border-radius:8px;
            border:1px solid #334155;
        ">
            <b style="color:#facc15;">📌 Sources:</b><br>
            <span style="color:#e2e8f0;">
                {chat['s']}
            </span>
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )