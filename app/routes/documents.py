from fastapi import APIRouter
from app.services.vector_service import collection

router = APIRouter()

@router.get("/documents")
def list_documents():

    data = collection.get()

    docs = set()

    for meta in data["metadatas"]:
        docs.add(meta["source"])

    return {
        "documents": list(docs)
    }