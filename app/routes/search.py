from fastapi import APIRouter
from pydantic import BaseModel

from app.services.vector_service import (
    collection,
    get_embedding
)

router = APIRouter()


class SearchRequest(BaseModel):
    query: str


@router.post("/search")
def search_docs(data: SearchRequest):

    # 🔥 FIX: use API embedding instead of model.encode
    query_embedding = get_embedding(data.query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return {
        "query": data.query,
        "results": results["documents"][0] if results["documents"] else []
    }