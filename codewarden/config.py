import logging
from dataclasses import dataclass
from typing import Literal
from crewai import LLM

from codewarden.logger import LogLevel


@dataclass
class Configuration:
    env: Literal["PROD", "DEV", "PREPROD", "TEST"]
    log_level: LogLevel
    google_svc_creds_file: str

    model_name: str = "gemini-2.0-flash"

    def load_llm(self):
        self.llm = LLM(
            model=self.model_name or "gemini-2.0-flash",
            temperature=0.20,
            top_p=0.80,
            max_completion_tokens=384,
            max_tokens=512,
            frequency_penalty=1.0,
        )

    @property
    def logger(self) -> logging.Logger:
        logging.basicConfig(
            level=self.log_level,
            datefmt="%Y-%m-%d %H:%M:%S",
            style="%",
            format="[%(levelname)s]:%(name)s:%(asctime)s: %(message)s",
        )
        return logging.getLogger("Codewarden")
