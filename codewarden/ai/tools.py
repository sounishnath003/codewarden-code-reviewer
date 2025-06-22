import logging
import os
from pathlib import Path
import subprocess
from typing import Any
import typing
from crewai.tools import BaseTool
import requests


class ProjectWorkspaceStructureTool(BaseTool):
    name: str = "Get Project Folder Structure"
    description: str = (
        "Scans and analyzes the complete project workspace structure, including directories, files, and their organization while intelligently filtering out build artifacts, dependencies, and configuration files to provide a clean overview of the codebase architecture"
    )
    logger: logging.Logger = logging.getLogger("Codewarden")

    def _run(self, directory_path: str, exclude_files: typing.List[str] = [], *args: Any, **kwargs: Any) -> Any:
        self.logger.info("Analyzing directory structure: %s", directory_path)
        
        if not exclude_files:
            exclude_files = [
                "node_modules", "__pycache__", ".git", ".venv", "venv", "env",
                "*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll", "*.dylib",
                "*.log", "*.tmp", "*.temp", "*.cache", "*.lock",
                "*.min.js", "*.min.css", "*.map", "*.bundle.js",
                ".DS_Store", "Thumbs.db", ".idea", ".vscode",
                "*.egg-info", "dist", "build", "target", "bin", "obj",
                "pyproject.toml",
                ".env",
                "package.json",
                "package-lock.json",
                ".md",
                "yarn.lock",
                "pnpm-lock.yaml",
                "Cargo.lock",
                "go.mod",
                "go.sum",
                "requirements.txt",
                "Pipfile",
                "Pipfile.lock",
                "poetry.lock",
                "setup.py",
                "setup.cfg",
                "MANIFEST.in",
                ".gitignore",
                ".gitattributes",
                ".editorconfig",
                ".prettierrc",
                ".eslintrc",
                "tsconfig.json",
                "webpack.config.js",
                "vite.config.js",
                "rollup.config.js",
                "jest.config.js",
                "karma.conf.js",
                "mocha.opts",
                ".nycrc",
                ".coveragerc",
                "tox.ini",
                "pytest.ini",
                ".flake8",
                ".pylintrc",
                "mypy.ini",
                "bandit.yaml",
                "safety.yaml",
                "docker-compose.yml",
                "Dockerfile",
                ".dockerignore",
                "Makefile",
                "CMakeLists.txt",
                "build.gradle",
                "pom.xml",
                "composer.json",
                "composer.lock",
                "Gemfile",
                "Gemfile.lock",
                "Rakefile",
                "mix.exs",
                "mix.lock",
                "pubspec.yaml",
                "pubspec.lock",
                "cabal.project",
                "stack.yaml",
                "package.yaml",
                "shard.yml",
                "shard.lock",
                "vcpkg.json",
                "conanfile.txt",
                "conanfile.py",
                "vcpkg.json",
                "vcpkg-configuration.json",
                ".md",
            ]
        
        try:
            project_structure = self._scan_directory(directory_path, exclude_files)
            return {
                "directory_path": directory_path,
                "structure": project_structure,
                "summary": f"Project structure analyzed for {directory_path}. Found {len(project_structure)} relevant files/directories."
            }
        except Exception as e:
            self.logger.error("Error analyzing directory structure: %s", str(e))
            return {"error": f"Failed to analyze directory structure: {str(e)}"}

    def _scan_directory(self, path: str, exclude_patterns: typing.List[str]) -> typing.Dict[str, Any]:
        """Recursively scan directory and build structure tree"""
        structure = {}
        path_obj = Path(path)
        
        if not path_obj.exists() or not path_obj.is_dir():
            return {"error": f"Directory does not exist: {path}"}
        
        try:
            for item in path_obj.iterdir():
                # Skip if item matches any exclude pattern
                if self._should_exclude(item, exclude_patterns):
                    continue
                
                item_name = item.name
                if item.is_dir():
                    # Recursively scan subdirectories
                    sub_structure = self._scan_directory(str(item), exclude_patterns)
                    if sub_structure:
                        structure[item_name] = {
                            "type": "directory",
                            "contents": sub_structure
                        }
                else:
                    # Add file with basic info
                    structure[item_name] = {
                        "type": "file",
                        "size": item.stat().st_size,
                        "extension": item.suffix
                    }
        
        except PermissionError:
            self.logger.warning("Permission denied accessing: %s", path)
        except Exception as e:
            self.logger.error("Error scanning directory %s: %s", path, str(e))
        
        return structure

    def _should_exclude(self, item: Path, exclude_patterns: typing.List[str]) -> bool:
        """Check if item should be excluded based on patterns"""
        item_name = item.name
        item_path = str(item)
        
        for pattern in exclude_patterns:
            # Handle wildcard patterns
            if "*" in pattern:
                if pattern.startswith("*"):
                    if item_name.endswith(pattern[1:]):
                        return True
                elif pattern.endswith("*"):
                    if item_name.startswith(pattern[:-1]):
                        return True
            # Handle exact matches
            elif item_name == pattern or item_path.endswith(pattern):
                return True
            # Handle directory patterns
            elif pattern in item_path.split(os.sep):
                return True
        
        return False


class CodeReadTool(BaseTool):
    name: str = "Read Code"
    description: str = "Reads the code written in a file"
    excluded_filenames: typing.List[str] = [
        "pyproject.toml",
        ".env",
        "package.json",
        "package-lock.json",
        ".md",
        "yarn.lock",
        "pnpm-lock.yaml",
        "Cargo.lock",
        "go.mod",
        "go.sum",
        "requirements.txt",
        "Pipfile",
        "Pipfile.lock",
        "poetry.lock",
        "setup.py",
        "setup.cfg",
        "MANIFEST.in",
        ".gitignore",
        ".gitattributes",
        ".editorconfig",
        ".prettierrc",
        ".eslintrc",
        "tsconfig.json",
        "webpack.config.js",
        "vite.config.js",
        "rollup.config.js",
        "jest.config.js",
        "karma.conf.js",
        "mocha.opts",
        ".nycrc",
        ".coveragerc",
        "tox.ini",
        "pytest.ini",
        ".flake8",
        ".pylintrc",
        "mypy.ini",
        "bandit.yaml",
        "safety.yaml",
        "docker-compose.yml",
        "Dockerfile",
        ".dockerignore",
        "Makefile",
        "CMakeLists.txt",
        "build.gradle",
        "pom.xml",
        "composer.json",
        "composer.lock",
        "Gemfile",
        "Gemfile.lock",
        "Rakefile",
        "mix.exs",
        "mix.lock",
        "pubspec.yaml",
        "pubspec.lock",
        "cabal.project",
        "stack.yaml",
        "package.yaml",
        "shard.yml",
        "shard.lock",
        "vcpkg.json",
        "conanfile.txt",
        "conanfile.py",
        "vcpkg.json",
        "vcpkg-configuration.json",
        ".md",
    ]

    def _run(self, path: str) -> str:

        file = Path(path)
        if not file.exists():
            return (
                f"File {path} does not exist. No Recommendations should be generated."
            )

        for f in self.excluded_filenames:
            if f in path:
                return f"This file={path} is among special configration files, no need to read"

        return file.read_text()


class UpdateReadmeTool(BaseTool):
    name: str = "Github Readme Writer"
    description: str = (
        "Updates github readme file with latest feature and information as per the latest workspace"
    )

    def _run(self, updated_content: str, *args: Any, **kwargs: Any) -> Any:
        try:
            with open("README.md", "w+", encoding="utf-8") as file:
                file.write(updated_content)
                file.write("\n> Readme has been updated by Codewarden")
                file.close()

            return "Readme file has been updated"
        except Exception as e:
            return f"Failed to updated Readme file due to Error={e}"


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
            # Use configurable exclude patterns if available, otherwise fall back to defaults
            if not exclude_files:
                exclude_files = [
                    ":(exclude)docs/",
                    ":(exclude)uv.lock",
                    ":(exclude)**/*.md",
                    ":(exclude)README.md",
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


class GitHubRepoInfoTool(BaseTool):
    name: str = "Get GitHub Repository Info"
    description: str = (
        "Gets the GitHub repository name and current commit hash using git commands"
    )

    def _run(self) -> str:
        try:
            # Get repository name using git config and sed
            repo_cmd = "git config --get remote.origin.url | sed -E 's#(git@|https://)github.com[:/](.*)\.git#\\2#'"
            repo_result = subprocess.run(
                repo_cmd, shell=True, capture_output=True, text=True
            )

            if repo_result.returncode != 0:
                return f"Failed to get repository name: {repo_result.stderr}"

            repo_name = repo_result.stdout.strip()

            # Get current commit hash
            commit_cmd = "git rev-parse HEAD"
            commit_result = subprocess.run(
                commit_cmd, shell=True, capture_output=True, text=True
            )

            if commit_result.returncode != 0:
                return f"Failed to get commit hash: {commit_result.stderr}"

            commit_sha = commit_result.stdout.strip()

            return f"Repository: {repo_name}, Commit: {commit_sha}"

        except Exception as e:
            return f"Error getting GitHub repository info: {str(e)}"


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
            "body": f"[Codewarden] ✨: {message}",
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
