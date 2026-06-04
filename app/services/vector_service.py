import os
import chromadb
import google.generativeai as genai

# ---------- CONFIG ----------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

client = chromadb.Client()
collection = client.get_or_create_collection(name="documents")

# ---------- EMBEDDINGS ----------
def get_embedding(text):
    result = genai.embed_content(
        model="models/embedding-001",
        content=text
    )
    return result["embedding"]

# ---------- CHUNKING ----------
def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# ---------- STORE DOC ----------
def store_document(text, filename):
    chunks = chunk_text(text)

    embeddings = [get_embedding(chunk) for chunk in chunks]

    ids = [f"{filename}_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"source": filename} for _ in chunks]
    )

    return len(chunks)