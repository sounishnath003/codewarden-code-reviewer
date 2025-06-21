import logging
import os
from pathlib import Path
import subprocess
from typing import Any
from crewai.tools import BaseTool
import requests


class ProjectWorkspaceAnalyzer(BaseTool):
    name: str = "Project Workpace Analyzer"
    description: str = (
        "Understands the whole project context (structure, modules, purpose)"
    )
    logger: logging.Logger = logging.getLogger("Codewarden")

    def _run(self, directory_path: str, *args: Any, **kwargs: Any) -> Any:
        self.logger.info("directory_path: %s", directory_path)
        return f"It is a Python + UV based project in directory {directory_path}. It is an AI agentic workflow"


class CodeReadTool(BaseTool):
    name: str = "Read Code"
    description: str = "Reads the code written in a file"

    def _run(self, path: str) -> str:
        file = Path(path)
        if not file.exists():
            return f"File {path} does not exist."
        return file.read_text()


class GitDiffTool(BaseTool):
    name: str = "Git Diff Tool"
    description: str = "Fetches the latest git diff between two latest commits"

    logger: logging.Logger = logging.getLogger("Codewarden")

    def _run(
        self,
        start_commit: str = "HEAD~1",
        end_commit: str = "HEAD",
        exclude_files: list[str] = [],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        try:
            # Build the git diff command with proper argument handling
            cmd = ["git", "diff", f"{start_commit}...{end_commit}"]
            # add exclude_files if None or length is zero
            if not exclude_files or len(exclude_files) == 0:
                exclude_files = [
                    ":(exclude)docs/",
                    ":(exclude)uv.lock",
                    ":(exclude)**/*.md",
                    ":(exclude)package-lock.json",
                ]
            # Extend the command with exclude patterns
            cmd.extend(exclude_files)

            result = subprocess.run(
                cmd,
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


class PRDiffTool(BaseTool):
    name: str = "Get PR Diff"
    description: str = "Fetches the diff from a GitHub pull request"

    def _run(self, repo: str, pr_number: int) -> str:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            return "GITHUB_TOKEN not set."

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3.diff",
        }
        url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
        response = requests.get(url, headers=headers)
        return response.text if response.ok else response.text


class TestScannerTool(BaseTool):
    name: str = "find_tests"
    description: str = "Finds test files or test functions related to a file or module"

    def _run(self, path: str) -> str:
        try:
            test_path = f"tests/{os.path.basename(path)}"
            if os.path.exists(test_path):
                return f"Test file exists: {test_path}"
            return f"No test results found for {path}"
        except Exception as e:
            return f"No test results found"


class StaticAnalysisTool(BaseTool):
    name: str = "Run Static Code Analysis"
    description: str = "Runs static analysis (e.g., pylint) on a file"
    logger: logging.Logger = logging.getLogger("Codewarden")

    def _run(self, file_path: str) -> str:
        self.logger.info("running pylint on file_path=%s", file_path)
        try:
            output = subprocess.check_output(
                ["pylint", file_path], stderr=subprocess.STDOUT
            )
            return output.decode()
        except subprocess.CalledProcessError as e:
            return e.output.decode()


class GitHubPRCommentTool(BaseTool):
    name: str = "Create Github PR Comment"
    description: str = "Posts a comment on a GitHub PR"

    def _run(
        self, repo: str, pr_number: int, path: str, position: int, message: str
    ) -> str:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            return "GITHUB_TOKEN not set."

        url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/comments"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        payload = {"body": message, "path": path, "position": position}

        response = requests.post(url, json=payload, headers=headers)
        return f"Posted comment to {path}:{position}" if response.ok else response.text


class GitHubCommitCommentTool(BaseTool):
    name: str = "Github Commit Comment"
    description: str = "Posts a comment on a GitHub commit"

    def _run(
        self, repo: str, commit_sha: str, path: str, position: int, message: str
    ) -> str:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            return "GITHUB_TOKEN is not set."

        url = f"https://api.github.com/repos/{repo}/commits/{commit_sha}/comments"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }

        payload = {
            "body": message,
            "path": path,
            "position": position,  # Position in diff, not line number in file!
            "commit_id": commit_sha,
        }

        response = requests.post(url, json=payload, headers=headers)
        return (
            f"✅ Comment posted: {message[:50]}..."
            if response.ok
            else f"❌ Failed: {response.text}"
        )
