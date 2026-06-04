from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.search import router as search_router
from app.routes.chat import router as chat_router
from app.routes.documents import router as documents_router

app = FastAPI(title="Enterprise AI Knowledge Assistant")

app.include_router(upload_router)
app.include_router(search_router)
app.include_router(chat_router)
app.include_router(documents_router)

@app.get("/")
def home():
    return {"message": "API Running Successfully"}