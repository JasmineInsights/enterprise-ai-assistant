from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.services.vector_service import get_embedding, collection
from app.services.llm_service import ask_gemini
from app.services.memory_service import add_message, get_history

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    document: Optional[str] = None


@router.post("/chat")
def chat(data: ChatRequest):

    query_embedding = get_embedding(data.question)

    if data.document:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
            where={"source": data.document}
        )
    else:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )

    documents = results["documents"][0] if results.get("documents") else []
    metadatas = results["metadatas"][0] if results.get("metadatas") else []

    context = "\n\n".join(documents)

    history = get_history()

    answer = ask_gemini(context, data.question, history)

    add_message("user", data.question)
    add_message("assistant", answer)

    sources = list(set(meta["source"] for meta in metadatas if meta.get("source")))

    return {
        "question": data.question,
        "answer": answer,
        "sources": sources
    }