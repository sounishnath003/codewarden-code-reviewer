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
