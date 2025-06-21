from crewai import Task

from codewarden.ai.agents import CodeReviewAgent
from codewarden.ai.base import BaseCodewardenAgent, BaseCodewardenTask
from codewarden.core.config import Configuration


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
                "A list of review comments in markdown format. Each comment should include the issue, "
                "the affected line or section, and a recommended fix or improvement."
            ),
            async_execution=False,
        )
