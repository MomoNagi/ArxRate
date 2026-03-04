import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
from src.arxrate.crew import ArxRateCrew

def run():
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    print(f"Connexion à Ollama : {base_url} (Modèle : {model})")

    topics = input("Quels sujets de recherche ArXiv voulez-vous explorer ? (ex: 'LLM agents') : ")
    max_results = input("Nombre maximum de résultats (par défaut 5) : ") or "5"

    inputs = {
        "topics": topics,
        "max_results": int(max_results)
    }
    os.makedirs("outputs", exist_ok=True)
    
    print(f"## Lancement de la veille sur : {topics}...")
    ArxRateCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()