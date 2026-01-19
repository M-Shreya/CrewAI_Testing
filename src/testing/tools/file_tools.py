from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import os

class FileReadInput(BaseModel):
    file_path: str = Field(..., description="The path to the file to read.")

class FileReadTool(BaseTool):
    name: str = "FileReadTool"
    description: str = "Reads the content of a file."
    args_schema: Type[BaseModel] = FileReadInput

    def _run(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='utf-16') as f:
                    return f.read()
            except Exception as e:
                return f"Error reading file with utf-16: {e}"
        except Exception as e:
            return f"Error reading file: {e}"

class FileWriteInput(BaseModel):
    file_path: str = Field(..., description="The path to the file to write.")
    content: str = Field(..., description="The content to write to the file.")

class FileWriteTool(BaseTool):
    name: str = "FileWriteTool"
    description: str = "Writes content to a file. Useful for creating test files."
    args_schema: Type[BaseModel] = FileWriteInput

    def _run(self, file_path: str, content: str) -> str:
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file: {e}"
