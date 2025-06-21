import logging
import subprocess
from typing import Any
from crewai.tools import BaseTool


class ProjectWorkspaceAnalyzer(BaseTool):
    name: str = "Project Workpace Analyzer"
    description: str = (
        "Understands the whole project context (structure, modules, purpose)"
    )
    logger: logging.Logger = logging.getLogger("Codewarden")

    def _run(self, directory_path: str, *args: Any, **kwargs: Any) -> Any:
        self.logger.info("directory_path: %s", directory_path)
        return f"It is a Python + UV based project in directory {directory_path}. It is an AI agentic workflow"


class GitDiffTool(BaseTool):
    name: str = "Git Diff Tool"
    description: str = "Fetches the latest git diff between two latest commits"

    logger: logging.Logger = logging.getLogger("Codewarden")

    def _run(
        self,
        start_commit: str = "HEAD~1",
        end_commit: str = "HEAD",
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        try:
            result = subprocess.run(
                ["git", "diff", f"{start_commit}...{end_commit}"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error("Failed to get git diff: %s", e.stderr or str(e))
            return f"Error fetching git diff: {e.stderr or str(e)}"
        except Exception as ex:
            self.logger.error("Unexpected error in GitDiffTool: %s", str(ex))
            return f"Unexpected error: {str(ex)}"
