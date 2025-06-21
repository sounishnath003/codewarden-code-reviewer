# Codewarden

Codewarden is an AI-powered code review tool that helps developers identify code issues, maintainability concerns, and ensure adherence to coding standards. It aims to use a combination of static analysis, test coverage analysis, and AI agents to provide comprehensive code reviews.

## Features

*   **AI-Powered Code Review:** Uses AI agents to analyze code and identify potential issues.
*   **Git Integration:** Analyzes Git diffs to focus on changes.
*   **Static Analysis:** Performs static analysis to detect code quality issues.
*   **Test Coverage Analysis:** Checks test coverage to ensure code is properly tested.
*   **GitHub Integration:** Aims to generate comments for GitHub pull requests.

## Installation

```bash
pip install python-dotenv
pip install uvloop
pip install click
pip install crewai
```

## Usage

```bash
# Example usage (assuming a CLI entry point)
# make run
```

## Project Structure

```
codewarden/
├── ai/
│   ├── agents.py  # Defines the AI agents for code review
│   ├── base.py    # Base classes for AI agents
│   └── tools.py   # Tools used by the AI agents
├── core/
│   └── config.py  # Configuration management
├── hooks/
│   └── prehooks.py # Pre-commit hooks
├── command/
│   └── logger.py # Logging setup
└── README.md      # This file
```

## Key Components (Planned)

*   **AI Agents:** The `ai/` directory will contain modules defining the AI agents used for code review. It will likely use the `crewai` library to create agents with specific roles, goals, and tools. Examples of agents might include:
    *   `WorkspaceContextAgent`: Understands the project structure and coding patterns.
    *   `CodeReviewAgent`: Identifies code issues, maintainability concerns, and adherence to standards.
    *   `CodeTestAgent`: Verifies that all new or changed code is covered by tests.
    *   `GithubCommentAgent`: Generates comments for GitHub pull requests.
*   **AI Tools:** The `ai/` directory will likely contain modules defining tools that the AI agents use. These tools could include:
    *   `CodeReadTool`: Reads the code written in a file.
    *   `UpdateReadmeTool`: Updates the README file.
    *   `GitDiffTool`: Fetches Git diffs between commits.
    *   `PRDiffTool`: Fetches the diff from a GitHub pull request.
    *   `TestScannerTool`: Finds test files or test functions related to a file or module.
    *   `StaticAnalysisTool`: Runs static analysis (e.g., pylint) on a file.
    *   `GitHubPRCommentTool`: Posts a comment on a GitHub pull request.
    *   `GitHubCommitCommentTool`: Posts a comment on a GitHub commit.
*   **Configuration:** The `core/` directory will likely contain modules for managing the project's configuration settings.
> Readme has been updated by Codewarden