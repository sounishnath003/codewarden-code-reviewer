from crewai import Task

from codewarden.ai.agents import CodeReviewAgent
from codewarden.ai.base import BaseCodewardenAgent, BaseCodewardenTask


class CodeReviewTask(BaseCodewardenTask):
    def __init__(self, agent: BaseCodewardenAgent) -> None:
        super().__init__()
        self.agent = agent

    @property
    def task(self) -> Task:
        return Task(
            agent=self.agent,
            description=(
                "Analyze the following Git diff to identify any code issues, performance problems, "
                "violations of best practices, or missing documentation. Make sure to be specific, "
                "cite line numbers, and suggest improvements where appropriate."
            ),
            expected_output=(
                "A list of review comments in markdown format directly no need of ```markdown. Each comment should include the issue, "
                "the affected line or section, and a recommended fix or improvement. "
                "Must mention the filepath for which you are generating comments,fix, improvements or recommendation"
            ),
            async_execution=False,
        )


class WorkspaceContextTask(BaseCodewardenTask):
    def __init__(self, agent: BaseCodewardenAgent) -> None:
        super().__init__()
        self.agent = agent

    @property
    def task(self) -> Task:
        return Task(
            agent=self.agent,
            description="Scan the project structure and summarize the key components, design patterns, and technologies used.",
            expected_output="A markdown summary of the project's architecture and purpose.",
            async_execution=False,
        )


class UpdateReadmeTask(BaseCodewardenTask):
    def __init__(self, agent: BaseCodewardenAgent) -> None:
        super().__init__()
        self.agent = agent

    @property
    def task(self) -> Task:
        return Task(
            agent=self.agent,
            description=(
                "Analyze the current project workspace and update the README.md file with the latest "
                "project information, features, and structure. Ensure the README reflects the current "
                "state of the codebase and includes proper documentation for users and contributors."
            ),
            expected_output=(
                "Updated README.md content that includes: project description, installation instructions, "
                "usage examples, project structure, and any other relevant documentation. "
                "The content should be well-formatted markdown ready to be written to README.md."
            ),
            async_execution=False,
        )


class CodeTestTask(BaseCodewardenTask):
    def __init__(self, agent: BaseCodewardenAgent) -> None:
        super().__init__()
        self.agent = agent

    @property
    def task(self) -> Task:
        return Task(
            agent=self.agent,
            description="Analyze the changed code and determine whether it is tested or lacks test coverage.",
            expected_output="List of functions/classes lacking tests and suggestions to improve coverage.",
            async_execution=False,
        )


class GithubCommentTask(BaseCodewardenTask):
    def __init__(self, agent: BaseCodewardenAgent) -> None:
        super().__init__()
        self.agent = agent

    @property
    def task(self) -> Task:
        return Task(
            agent=self.agent,
            description="Convert the review output into structured GitHub comments with filename, line number, and message.",
            expected_output="Lists of JSON-formatted GitHub comments with path, position, commit_id and message.",
            async_execution=False,
        )
