import subprocess
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class TestRunnerInput(BaseModel):
    test_file: str = Field(..., description="The path to the test file to run.")

class TestRunnerTool(BaseTool):
    name: str = "TestRunnerTool"
    description: str = "Runs pytest on a given file and returns the output."
    args_schema: Type[BaseModel] = TestRunnerInput

    def _run(self, test_file: str) -> str:
        try:
            # Running pytest and capturing output
            result = subprocess.run(
                [
  'pytest',
  test_file,
  '--cov=src/testing/target',
  '--cov-report=term',
  '--cov-report=xml'
]
,
                capture_output=True,
                text=True
            )
            return f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        except Exception as e:
            return f"Error running tests: {e}"
