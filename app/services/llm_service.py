import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
import os
print("Loaded Key:", os.getenv("GEMINI_API_KEY"))

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask_gemini(context, question,history):

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

Conversation History:
{history}

Context:
{context}

Question:
{question}

Answer:
"""

    response = model.generate_content(prompt)

    return response.text