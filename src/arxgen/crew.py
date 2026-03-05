import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM
from arxgen.tools.arxiv_tool import ArxivSearchTool
import os

@CrewBase
class ArxGenCrew:
    """Crew to research and analyse arxiv papers based on a query"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        self.ollama_llm = LLM(
            model=f"ollama/{os.getenv('OLLAMA_MODEL', 'llama3.2')}",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0.1,
        )
    
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=[ArxivSearchTool()],
            llm=self.ollama_llm,
            verbose=True,
            max_iter=3,
            allow_delegation=False
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["analyst"],
            llm=self.ollama_llm,
            verbose=True
        )

    @task
    def task_retrieval(self) -> Task:
        return Task(
            config=self.tasks_config["task_retrieval"],
            agent=self.researcher()
        )

    @task
    def task_analyse(self) -> Task:
        return Task(
            config=self.tasks_config["task_analyse"],
            agent=self.analyst(),
            context=[self.task_retrieval()],
            output_file="src/arxgen/outputs/report.md"
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )