import os
from dotenv import load_dotenv  
from arxgen.crew import ArxGenCrew

load_dotenv()

def run():
    base_url = os.getenv("OLLAMA_BASE_URL")
    model = os.getenv("OLLAMA_MODEL")
    print(f"Connexion à Ollama : {base_url} (Modèle : {model})")

    topics = input("Quels sujets de recherche ArXiv voulez-vous explorer ? (ex: 'LLM agents') : ")
    max_results = input("Nombre maximum de résultats (par défaut 5) : ") or "5"

    inputs = {
        "topics": topics,
        "max_results": int(max_results)
    }
    os.makedirs("src/arxgen/outputs", exist_ok=True)

    print(f"## Lancement de la veille sur : {topics}...")
    ArxGenCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()