from fastapi import APIRouter
from pydantic import BaseModel

from app.services.vector_service import (
    collection,
    model as embedding_model
)

from app.services.llm_service import (
    ask_gemini
)

from app.services.memory_service import (
    add_message,
    get_history
)
router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    document: str | None = None

@router.post("/chat")
def chat(data: ChatRequest):

    query_embedding = embedding_model.encode(
        data.question
    ).tolist()

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

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n\n".join(documents)

    history = get_history()

    answer = ask_gemini(
        context,
        data.question,
        history
    )

    add_message("user", data.question)
    add_message("assistant", answer)

    sources = list(set(
        meta["source"]
        for meta in metadatas
    ))

    return {
        "question": data.question,
        "answer": answer,
        "sources": sources
    }