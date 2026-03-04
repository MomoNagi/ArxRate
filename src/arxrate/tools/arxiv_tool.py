import arxiv
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class ArxivSearchInput(BaseModel):
    """Schéma d'entrée pour l'outil de recherche Arxiv."""

    query: str = Field(..., description="Les mots-clés de recherche")
    max_results: int = Field(default=5, description="Le nombre maximum d'articles à récupérer")

class ArxivSearchTool(BaseTool):
    name: str = "Extracteur de recherche Arxiv"
    description: str = (
        "Outil pour rechercher des articles sur Arxiv en fonction de mots-clés."
    )
    args_schema: Type[BaseModel] = ArxivSearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        try:
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            results = []
            query_results = client.results(search)
            for result in query_results:
                authors = ", ".join(author.name for author in result.authors)
                paper_info = (
                    f"Title: {result.title}\n"
                    f"Authors: {authors}\n"
                    f"Published: {result.published.date()}\n"
                    f"Summary: {result.summary}\n"
                    f"URL: {result.entry_id}\n"
                    f"{'-'*20}"
                )
                results.append(paper_info)

            if not results:
                return f"Aucun article trouvé pour la recherche de ces mots-clés : {query}"
                
            return "\n\n".join(results)
        
        except Exception as e:
            return f"Erreur lors de l'interrogation de la base d'ArXiv : {str(e)}"