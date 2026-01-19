from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from testing.tools.file_tools import FileReadTool, FileWriteTool
from testing.tools.test_tools import TestRunnerTool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read API key from environment (Jenkins-safe)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@CrewBase
class Testing():

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    tracing = False   # disable tracing for CI stability

    @agent
    def workflow_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['workflow_analyst'],
            tools=[FileReadTool()],
            verbose=True,
            llm=LLM(
                model="groq/llama-3.1-8b-instant",
                api_key=GROQ_API_KEY,
                temperature=0.1,
                max_tokens=256
            )
        )

    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
            tools=[FileWriteTool()],
            verbose=True,
            llm=LLM(
                model="groq/llama-3.1-8b-instant",
                api_key=GROQ_API_KEY,
                temperature=0.1,
                max_tokens=256
            )
        )

    @agent
    def qa_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_manager'],
            tools=[TestRunnerTool()],
            verbose=True,
            llm=LLM(
                model="groq/llama-3.1-8b-instant",
                api_key=GROQ_API_KEY,
                temperature=0.1,
                max_tokens=256
            )
        )

    @task
    def code_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_analysis_task']
        )

    @task
    def test_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_generation_task']
        )

    @task
    def test_execution_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_execution_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
