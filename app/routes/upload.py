from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import extract_text_from_pdf
from app.services.vector_service import store_document
from app.services.docx_service import extract_text_from_docx
from app.services.pptx_service import extract_text_from_pptx
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    file_extension = file.filename.split(".")[-1].lower()

    if file_extension == "pdf":
        extracted_text = extract_text_from_pdf(file_path)

    elif file_extension == "docx":
        extracted_text = extract_text_from_docx(file_path)

    elif file_extension == "pptx":
        extracted_text = extract_text_from_pptx(file_path)

    else:
        return {
            "error": "Only PDF, DOCX, and PPTX files are supported"
        }

    chunks_stored = store_document(
        extracted_text,
        file.filename
    )

    return {
        "filename": file.filename,
        "characters_extracted": len(extracted_text),
        "chunks_stored": chunks_stored,
        "preview": extracted_text[:500]
    }