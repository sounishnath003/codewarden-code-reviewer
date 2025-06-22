import typing
from crewai import Agent
from crewai.tools import BaseTool

from codewarden.ai.base import BaseCodewardenAgent
from codewarden.core.config import Configuration
from codewarden.ai.tools import (
    CodeReadTool,
    GitDiffTool,
    GitHubCommitCommentTool,
    GitHubPRCommentTool,
    GitHubRepoInfoTool,
    PRDiffTool,
    StaticAnalysisTool,
    TestScannerTool,
    UpdateReadmeTool,
    ProjectWorkspaceStructureTool
)


class WorkspaceContextAgent(BaseCodewardenAgent):
    def __init__(
        self,
        conf: Configuration,
        tools: typing.List[BaseTool] = [ProjectWorkspaceStructureTool(), CodeReadTool(), UpdateReadmeTool()],
    ) -> None:
        super().__init__()
        self.conf = conf
        self.tools = tools

        self.agent = Agent(
            role="Workspace Context Analyzer",
            goal="Understand the project structure, architecture and coding patterns of this project",
            backstory="You are a senior software architecture with deep experience in analyzing codebases.",
            verbose=True,
            tools=self.tools,
            llm=conf.llm,
        )


class CodeReviewAgent(BaseCodewardenAgent):
    def __init__(
        self,
        conf: Configuration,
        tools: typing.Optional[typing.List[BaseTool]] = None,
    ) -> None:
        super().__init__()
        self.conf = conf
        if tools is None:
            tools = [
                GitDiffTool(config=conf),
                # PRDiffTool(),
                StaticAnalysisTool(),
            ]
        self.tools = tools

        self.agent = Agent(
            role="Code Reviewer",
            goal="Identify code issues, maintainability concerns, and adherence to standards",
            backstory="An experienced developer trained to assess PR diffs for quality and clarity.",
            tools=self.tools,
            verbose=True,
            llm=conf.llm,
        )


class CodeTestAgent(BaseCodewardenAgent):
    def __init__(
        self, conf: Configuration, tools: typing.List[BaseTool] = [TestScannerTool()]
    ) -> None:
        super().__init__()
        self.conf = conf
        self.tools = tools

        self.agent = Agent(
            role="Test Coverage Checker",
            goal="Verify that all new or changed code is covered by tests",
            backstory="An automated QA engineer that ensures each PR maintains high test coverage.",
            tools=self.tools,
            verbose=True,
            llm=conf.llm,
        )


class GithubCommentAgent(BaseCodewardenAgent):
    def __init__(
        self,
        conf: Configuration,
        tools: typing.List[BaseTool] = [
            GitHubRepoInfoTool(),
            GitHubCommitCommentTool(),
            # GitHubPRCommentTool(),
        ],
    ) -> None:
        super().__init__()
        self.conf = conf
        self.tools = tools

        self.agent = Agent(
            role="GitHub Comment Writer",
            goal="Turn code review feedback into GitHub comments",
            backstory="A GitHub-savvy assistant that formats review insights into GitHub-ready comments.",
            tools=self.tools,
            verbose=True,
            llm=conf.llm,
        )
