from abc import ABC, abstractproperty
from crewai import Agent, Task
from codewarden.core.config import Configuration


class BaseCodewardenAgent(ABC):
    conf: Configuration
    agent: Agent


class BaseCodewardenTask(ABC):
    task: Task
