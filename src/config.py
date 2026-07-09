from dotenv import load_dotenv
import os
import langchain_ollama
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI

OLLAMA_MODEL = "llama3.1:8b"

# if you want to use gemini
def load_model():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found. Check your .env file.")
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key,
        temperature=0.2
    )
    return model

# def load_model():
#     model = langchain_ollama.ChatOllama(
#         model=OLLAMA_MODEL,
#         temperature=0,
#     )
#     return model