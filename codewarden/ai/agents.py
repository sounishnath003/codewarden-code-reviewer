from crewai import Agent

from codewarden.ai.base import BaseCodewardenAgent
from codewarden.core.config import Configuration

# Initial thoughts what are the agents
#   project understanding agent
#   bughunter agent
#   security agent


class ProjectUnderstandingAgent(BaseCodewardenAgent):
    def __init__(self, conf: Configuration) -> None:
        super().__init__()
        self.conf = conf
        self.agent = Agent(
            role="Research Analyst",
            goal="Find and summarize information about specific topics",
            backstory="You are an experienced researcher with attention to detail",
            tools=[],
            verbose=True,
            llm=conf.llm,
        )
