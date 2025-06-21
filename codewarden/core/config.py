import os
import logging
import typing
from dataclasses import dataclass
from typing import Literal
from crewai import LLM

from codewarden.command.logger import LogLevel, LoggerFormat

type ProjectType = typing.Literal["NODEJS", "PYTHON", "JAVA", "UNKNOWN"]


@dataclass
class Configuration:
    env: Literal["PROD", "DEV", "PREPROD", "TEST"]
    log_level: LogLevel
    google_svc_creds_file: str

    model_name: str = "gemini-2.0-flash"

    @property
    def llm(self):
        self.logger.debug("creating the llm instance")
        return LLM(
            model=self.model_name or "gemini-2.0-flash",
            temperature=0.10,
            top_p=0.80,
            max_completion_tokens=384,
            max_tokens=512,
            frequency_penalty=1.0,
        )

    @property
    def logger(self) -> logging.Logger:
        logging.basicConfig(**LoggerFormat)
        return logging.getLogger("Codewarden")

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
