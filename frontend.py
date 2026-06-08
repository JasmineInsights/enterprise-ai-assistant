import streamlit as st
import requests
from html import escape

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
    .stApp {
        background-color: #0f172a;
        color: white;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 1100px;
    }

    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
        border-radius: 8px;
    }

    .stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }

    .stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #020617;
    }

    .source-box {
        background-color: #020617;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #334155;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "is_loading" not in st.session_state:
    st.session_state.is_loading = False


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("📁 Document Hub")

    uploaded_file = st.file_uploader(
        "Upload Document",
        type=["pdf", "docx", "pptx"]
    )

    if uploaded_file:
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
                    st.text(res.text[:500])

            except requests.exceptions.Timeout:
                st.error("Upload timeout. Try again with a smaller document.")

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend. Check if Render server is running.")

            except Exception as e:
                st.error(f"Upload failed: {e}")


# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align: center; color: #38bdf8;'>🤖 Enterprise AI Assistant</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: #94a3b8;'>Chat with your documents using AI</p>",
    unsafe_allow_html=True
)

st.divider()


# ---------------- CHAT INPUT FORM ----------------
with st.form("chat_form", clear_on_submit=True):
    question = st.text_input(
        "Ask anything from your documents...",
        placeholder="Example: Summarize this document..."
    )

    submitted = st.form_submit_button("🚀 Ask")


# ---------------- HANDLE CHAT ----------------
if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Thinking..."):
                res = requests.post(
                    f"{API_URL}/chat",
                    json={"question": question.strip()},
                    timeout=120
                )

            if res.status_code == 200:
                data = res.json()

                answer = data.get("answer", "")
                sources = data.get("sources", [])

                if not isinstance(sources, list):
                    sources = [str(sources)]

                st.session_state.chat_history.append({
                    "q": question.strip(),
                    "a": answer,
                    "s": sources
                })

            else:
                st.error(f"Backend Error: {res.status_code}")
                st.text(res.text[:800])

        except requests.exceptions.Timeout:
            st.error("Backend took too long to respond. Try a shorter question.")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to backend. Your Render app may be sleeping or down.")

        except Exception as e:
            st.error(f"Error: {e}")


# ---------------- CHAT DISPLAY ----------------
for chat in reversed(st.session_state.chat_history):

    with st.chat_message("user"):
        st.markdown(chat["q"])

    with st.chat_message("assistant"):
        # Safe rendering.
        # This allows markdown but does not run raw unsafe HTML.
        st.markdown(chat["a"])

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