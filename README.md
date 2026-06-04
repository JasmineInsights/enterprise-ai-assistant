# 🤖 Enterprise AI Knowledge Assistant

AI app that lets you upload documents (PDF, DOCX, PPTX) and chat with them using RAG + Gemini.

---

## 🚀 Features
- Upload documents
- Ask questions from documents
- AI answers using Gemini
- Uses vector database (ChromaDB)

---

## 🛠 Tech Stack
- FastAPI (backend)
- Streamlit (frontend)
- ChromaDB (vector DB)
- Sentence Transformers (embeddings)
- Google Gemini API

---

## ▶️ Run Project

### 1. Start backend
```bash
uvicorn app.main:app --reload