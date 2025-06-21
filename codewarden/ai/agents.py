import typing
from crewai import Agent
from crewai.tools import BaseTool

from codewarden.ai.base import BaseCodewardenAgent
from codewarden.core.config import Configuration
from codewarden.ai.tools import GitDiffTool

# Initial thoughts what are the agents
#   project understanding agent
#   bughunter agent
#   security agent


class CodeReviewAgent(BaseCodewardenAgent):
    def __init__(
        self, conf: Configuration, tools: typing.List[BaseTool] = [GitDiffTool()]
    ) -> None:
        super().__init__()
        self.conf = conf
        self.tools = tools

        self.agent = Agent(
            role="Code Reviewer",
            goal="Identify code issues, maintainability concerns, and adherence to standards",
            backstory="An experienced developer trained to assess PR diffs for quality and clarity.",
            tools=self.tools,
            verbose=True,
            llm=conf.llm,
        )
