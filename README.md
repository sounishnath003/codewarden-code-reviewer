# CodeWarden

CodeWarden is a tool designed to automate code review and improve code quality. It uses a combination of static analysis, Git diff analysis, and AI agents to identify code issues, maintainability concerns, and adherence to standards. It can also be used to update the README file and provide feedback as GitHub comments.

## Key Components

*   **`main.py`**: The entry point of the application, which initializes and runs the command-line interface.
*   **`codewarden/command/cli.py`**: Defines the command-line interface using `argparse`. It reads a YAML configuration file and initializes the `Crew` of agents and tasks.
*   **`codewarden/core/config.py`**: Defines the `Configuration` class, which stores configuration parameters such as environment, model name, log level, credentials, and exclude patterns. It also initializes a logger and configures a Language Model.
*   **`codewarden/ai/agents.py`**: Defines the AI agents used in the `CrewAI` workflow. These agents include:
    *   `WorkspaceContextAgent`: Analyzes the project structure.
    *   `CodeReviewAgent`: Identifies code issues.
    *   `CodeTestAgent`: Checks test coverage.
    *   `GithubCommentAgent`: Writes GitHub comments.
*   **`codewarden/ai/tasks.py`**: Defines the tasks performed by the agents. These tasks include code review, workspace context analysis, updating the README, checking test coverage, and writing GitHub comments.
*   **`codewarden/ai/tools.py`**: Defines the tools used by the agents to perform their tasks. These tools include:
    *   `CodeReadTool`
    *   `GitDiffTool`
    *   `GitHubCommitCommentTool`
    *   `GitHubPRCommentTool`
    *   `GitHubRepoInfoTool`
    *   `PRDiffTool`
    *   `StaticAnalysisTool`
    *   `TestScannerTool`
    *   `UpdateReadmeTool`
    *   `ProjectWorkspaceStructureTool`

## Design Patterns

*   **CrewAI**: The project uses the `crewAI` library to orchestrate the AI agents and tasks.
*   **Dataclasses**: The `Configuration` class uses a dataclass to store configuration parameters.

## Technologies Used

*   Python
*   `crewAI`
*   `argparse`
*   YAML
*   dataclasses
*   logging

## Project Purpose

The purpose of CodeWarden is to automate code review and improve code quality by using AI agents and various tools to analyze code, identify issues, and provide feedback.
> Readme has been updated by Codewarden