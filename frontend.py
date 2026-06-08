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
    /* Full app background */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem;
        max-width: 1100px;
        color: #f8fafc;
    }

    /* Force main text colors */
    .main,
    .block-container,
    .stMarkdown,
    .stText,
    .stCaption {
        color: #f8fafc !important;
    }

    .stMarkdown p,
    .stMarkdown span,
    .stMarkdown div,
    .stMarkdown li,
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown h4,
    .stMarkdown h5,
    .stMarkdown h6 {
        color: #f8fafc !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #020617;
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* Labels */
    label,
    .stTextInput label,
    .stFileUploader label {
        color: #f8fafc !important;
    }

    /* Text input */
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: #f8fafc !important;
        border: 1px solid #334155;
        border-radius: 8px;
    }

    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
    }

    /* File uploader */
    section[data-testid="stFileUploaderDropzone"] {
        background-color: #1e293b;
        border: 1px dashed #475569;
        color: #f8fafc;
        border-radius: 10px;
    }

    section[data-testid="stFileUploaderDropzone"] * {
        color: #f8fafc !important;
    }

    /* Buttons */
    .stButton > button,
    .stFormSubmitButton > button {
        background-color: #2563eb;
        color: #ffffff !important;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 600;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background-color: #1d4ed8;
        color: #ffffff !important;
        border: none;
    }

    /* Chat message containers */
    div[data-testid="stChatMessage"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
        color: #f8fafc !important;
    }

    div[data-testid="stChatMessage"] * {
        color: #f8fafc !important;
    }

    /* Expander / Sources */
    div[data-testid="stExpander"] {
        background-color: #020617;
        border: 1px solid #334155;
        border-radius: 8px;
    }

    div[data-testid="stExpander"] * {
        color: #f8fafc !important;
    }

    .streamlit-expanderHeader {
        color: #facc15 !important;
        background-color: #020617 !important;
    }

    /* Code blocks */
    code,
    pre {
        background-color: #020617 !important;
        color: #e2e8f0 !important;
        border-radius: 8px;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        color: #f8fafc !important;
    }

    div[data-testid="stAlert"] * {
        color: #f8fafc !important;
    }

    /* Divider */
    hr {
        border-color: #334155;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("📁 Document Hub")

    uploaded_file = st.file_uploader(
        "Upload Document",
        type=["pdf", "docx", "pptx"]
    )

    if uploaded_file:
        st.caption(f"Selected file: {uploaded_file.name}")

        if st.button("Upload Document"):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            try:
                with st.spinner("Uploading document..."):
                    res = requests.post(
                        f"{API_URL}/upload",
                        files=files,
                        timeout=60
                    )

                if res.status_code == 200:
                    data = res.json()

                    st.success("Uploaded successfully 🚀")

                    st.write("**Filename:**", data.get("filename", uploaded_file.name))
                    st.write("**Chunks Stored:**", data.get("chunks_stored", "N/A"))

                else:
                    st.error(f"Upload failed. Backend returned {res.status_code}")

                    if res.text:
                        st.code(res.text[:800])

            except requests.exceptions.Timeout:
                st.error("Upload timeout. Try again with a smaller document.")

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend. Your Render server may be sleeping or down.")

            except Exception as e:
                st.error(f"Upload failed: {e}")


# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center; color:#38bdf8;'>🤖 Enterprise AI Assistant</h1>
    <p style='text-align:center; color:#cbd5e1;'>Chat with your documents using AI</p>
    """,
    unsafe_allow_html=True
)

st.divider()


# ---------------- CHAT INPUT ----------------
with st.form("chat_form", clear_on_submit=True):
    question = st.text_input(
        "Ask anything from your documents...",
        placeholder="Example: Summarize this document..."
    )

    submitted = st.form_submit_button("🚀 Ask")


# ---------------- HANDLE CHAT REQUEST ----------------
if submitted:
    clean_question = question.strip()

    if not clean_question:
        st.warning("Please enter a question.")

    else:
        try:
            with st.spinner("Thinking..."):
                res = requests.post(
                    f"{API_URL}/chat",
                    json={"question": clean_question},
                    timeout=120
                )

            if res.status_code == 200:
                data = res.json()

                answer = data.get("answer", "")
                sources = data.get("sources", [])

                if not isinstance(sources, list):
                    sources = [str(sources)]

                st.session_state.chat_history.append({
                    "q": clean_question,
                    "a": answer,
                    "s": sources
                })

            else:
                st.error(f"Backend Error: {res.status_code}")

                if res.text:
                    st.code(res.text[:800])

        except requests.exceptions.Timeout:
            st.error("Backend took too long to respond. Try a shorter question.")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to backend. Your Render server may be sleeping or down.")

        except Exception as e:
            st.error(f"Error: {e}")


# ---------------- CHAT DISPLAY ----------------
if st.session_state.chat_history:
    st.subheader("💬 Chat History")

for chat in reversed(st.session_state.chat_history):

    with st.chat_message("user"):
        st.markdown(f"**🧑 You:**\n\n{chat['q']}")

    with st.chat_message("assistant"):
        # Important:
        # Do not use unsafe_allow_html=True here.
        # This prevents Gemini HTML output from breaking the UI.
        st.markdown(f"**🤖 AI:**\n\n{chat['a']}")

        sources = chat.get("s", [])

        if sources:
            with st.expander("📌 Sources"):
                for idx, source in enumerate(sources, start=1):
                    st.write(f"{idx}. {source}")
        else:
            st.caption("No sources returned.")


# ---------------- CLEAR CHAT ----------------
if st.session_state.chat_history:
    st.divider()

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()