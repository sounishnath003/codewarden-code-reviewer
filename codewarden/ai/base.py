from abc import ABC
import logging
from crewai import Agent, Task
from codewarden.core.config import Configuration
from crewai.tools import BaseTool
from typing import Optional

class BaseCodewardenAgent(ABC):
    conf: Configuration
    agent: Agent


class BaseCodewardenTask(ABC):
    task: Task

class BaseCodewardenTool(BaseTool):
    """Base tool class for Codewarden that includes Configuration support"""
    conf: Configuration