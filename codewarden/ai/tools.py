import logging
import subprocess
from typing import Any
from crewai.tools import BaseTool


class T(BaseTool):
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

    def _run(
        self,
        start_commit: str = "HEAD~1",
        end_commit: str = "HEAD",
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        return subprocess.check_output(
            ["git", "diff", f"{start_commit}...{end_commit}"]
        ).decode()
