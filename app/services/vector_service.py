import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.Client()
collection = client.get_or_create_collection(
    name="documents"
)

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def chunk_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def store_document(text, filename):

    chunks = chunk_text(text)

    embeddings = model.encode(chunks).tolist()

    ids = [
        f"{filename}_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {"source": filename}
            for _ in chunks
        ]
    )

    return len(chunks)