from fastapi import APIRouter
from pydantic import BaseModel

from app.services.vector_service import (
    collection,
    model
)

router = APIRouter()


class SearchRequest(BaseModel):
    query: str


@router.post("/search")
def search_docs(data: SearchRequest):

    query_embedding = model.encode(
        data.query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return {
        "query": data.query,
        "results": results["documents"][0]
    }