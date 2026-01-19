from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from testing.tools.file_tools import FileReadTool, FileWriteTool
from testing.tools.test_tools import TestRunnerTool
import os
from dotenv import load_dotenv

load_dotenv()


@CrewBase
class Testing():

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    tracing= True

    @agent
    def workflow_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['workflow_analyst'],
            tools=[FileReadTool()],
            verbose=True,
            llm=LLM(model="groq/llama-3.3-70b-versatile", api_key="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")
        )

    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
            tools=[FileWriteTool()],
            verbose=True,
            llm=LLM(model="groq/llama-3.3-70b-versatile", api_key="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")
        )

    @agent
    def qa_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_manager'],
            tools=[TestRunnerTool()],
            verbose=True,
            llm=LLM(model="groq/llama-3.3-70b-versatile", api_key="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")
        )

    @task
    def code_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_analysis_task'],
        )

    @task
    def test_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_generation_task'],
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
            verbose=True,
        )



