# 🤖 Enterprise AI Knowledge Assistant

An AI-powered document intelligence application that allows users to upload PDF, DOCX, and PPTX files and chat with them using Retrieval-Augmented Generation (RAG), ChromaDB, and Google Gemini.

## 🌐 Live Demo

**Frontend (Streamlit)**
https://enterprise-ai-assistant-xr9bm23nko8fhuhjdjh7ix.streamlit.app/
**Backend API (Render)**
https://enterprise-ai-assistant-43az.onrender.com

**API Documentation**
https://enterprise-ai-assistant-43az.onrender.com/docs

---

## 🚀 Features

* Upload PDF, DOCX, and PPTX documents
* Extract and process document content automatically
* Semantic search using Gemini Embeddings
* Retrieval-Augmented Generation (RAG)
* AI-powered question answering using Gemini 2.5 Flash
* Source-aware responses
* FastAPI backend and Streamlit frontend
* ChromaDB vector database integration

## 🛠 Tech Stack

### Backend

* FastAPI
* ChromaDB
* Google Gemini API
* Python

### Frontend

* Streamlit

### AI Components

* Gemini Embeddings (`gemini-embedding-001`)
* Gemini 2.5 Flash
* Retrieval-Augmented Generation (RAG)

## 📂 Supported File Types

* PDF
* DOCX
* PPTX

## ▶️ Run Locally

### Clone Repository

```bash
git clone <repository-url>
cd enterprise-ai-assistant
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

### Start Backend

```bash
uvicorn app.main:app --reload
```

### Start Frontend

```bash
streamlit run frontend.py
```

## 📌 Workflow

1. Upload a document
2. Extract text from the uploaded file
3. Generate embeddings using Gemini Embeddings
4. Store vectors in ChromaDB
5. Retrieve relevant document chunks for a query
6. Generate context-aware responses using Gemini 2.5 Flash
7. Return answers along with source documents

## 🚀 Deployment

* Backend: Render
* Frontend: Streamlit Community Cloud
