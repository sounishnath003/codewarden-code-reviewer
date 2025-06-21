from abc import ABC
from crewai import Agent
from codewarden.core.config import Configuration


class BaseCodewardenAgent(ABC):
    conf: Configuration
    agent: Agent
