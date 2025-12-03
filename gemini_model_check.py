import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERRORE: Chiave API non trovata nel file .env")
else:
    genai.configure(api_key=api_key)
    print("--- Modelli Disponibili per la tua Chiave ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Nome: {m.name}")
    except Exception as e:
        print(f"Errore di connessione: {e}")