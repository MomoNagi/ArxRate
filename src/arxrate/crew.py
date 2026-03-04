from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_ollama import ChatOllama
from arxrate.tools.arxiv_tool import ArxivSearchTool
import os

@CrewBase
class ArxRateCrew:
    """Crew to research and analyse arxiv papers based on a query"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        self.ollama_llm = ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0.1,
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=[ArxivSearchTool()],
            llm=self.ollama_llm,
            verbose=True
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["analyst"],
            llm=self.ollama_llm,
            verbose=True
        )

    @task
    def retrieval_task(self) -> Task:
        return Task(
            config=self.tasks_config["retrieval_task"],
            agent=self.researcher()
        )

    @task
    def extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config["extraction_task"],
            agent=self.analyst(),
            context=[self.retrieval_task()],
            output_file="src/arxrate/outputs/report.md"
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )