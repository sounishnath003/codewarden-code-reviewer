import os
import logging
import typing
from dataclasses import dataclass, field
from typing import Literal
from crewai import LLM

from codewarden.command.logger import LogLevel, LoggerFormat, init_logger

type ProjectType = typing.Literal["NODEJS", "PYTHON", "JAVA", "UNKNOWN"]


@dataclass
class Configuration:
    env: Literal["PROD", "DEV", "PREPROD", "TEST"]
    model_name: str
    log_level: LogLevel
    google_svc_creds_file: str
    github_token: str
    global_exclution_files_folders: typing.List[str] = field(
        default_factory=lambda: [
            "node_modules",
            "__pycache__",
            ".git",
            ".venv",
            "venv",
            "env",
            "*.pyc",
            "*.txt",
            "*.pyo",
            "*.pyd",
            "*.so",
            "*.dll",
            "*.dylib",
            "*.log",
            "*.tmp",
            "*.temp",
            "*.cache",
            "*.lock",
            "*.min.js",
            "*.min.css",
            "*.map",
            "*.bundle.js",
            ".DS_Store",
            "Thumbs.db",
            ".idea",
            ".vscode",
            "*.egg-info",
            "dist",
            "build",
            "target",
            "bin",
            "obj",
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
    )
    
    git_diff_exclude_patterns: typing.List[str] = field(
        default_factory=lambda: [
            ":(exclude)docs/",
            ":(exclude)uv.lock",
            ":(exclude)**/*.md",
            ":(exclude)README.md",
            ":(exclude)package-lock.json",
        ]
    )
    logger: logging.Logger = field(default=init_logger())

    def __post_init__(self):
        # Only initialize the logger if it hasn't been set
        if self.logger is None:
            # Check if root logger has handlers, if not, configure it
            root_logger = logging.getLogger()
            if not root_logger.handlers:
                logging.basicConfig(**LoggerFormat)
            self.logger = logging.getLogger("Codewarden")

    @property
    def llm(self):
        return LLM(
            model=self.model_name or "gemini-2.0-flash",
            top_p=0.80,
            max_tokens=768,
            temperature=0.10,
            frequency_penalty=1.0,
            max_completion_tokens=512,
            vertex_credentials=open(self.google_svc_creds_file, "r+").read(),
        )

    def detect_project_type(self, path: str = ".") -> ProjectType:
        self.logger.info("trying to identify the project workspace")
        if os.path.exists(os.path.join(path, "package.json")):
            return "NODEJS"
        elif os.path.exists(os.path.join(path, "pyproject.toml")) or os.path.exists(
            os.path.join(path, "requirements.txt")
        ):
            return "PYTHON"
        elif os.path.exists(os.path.join(path, "application.properties")):
            return "JAVA"

        return "UNKNOWN"
