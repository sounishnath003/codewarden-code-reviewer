# Codewarden

Codewarden is an AI-powered code review tool that helps developers identify code issues, maintainability concerns, and ensure adherence to coding standards. It uses a combination of static analysis, test coverage analysis, and AI agents to provide comprehensive code reviews.

## Features

*   **AI-Powered Code Review:** Uses AI agents to analyze code and identify potential issues.
*   **Git Integration:** Analyzes Git diffs to focus on changes.
*   **Static Analysis:** Performs static analysis to detect code quality issues.
*   **Test Coverage Analysis:** Checks test coverage to ensure code is properly tested.
*   **GitHub Integration:** Generates comments for GitHub pull requests.

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
python codewarden.py --path . --output review.md --model gpt-4
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

## Agents

*   **Workspace Context Analyzer:** Understands the project structure and coding patterns.
*   **Code Reviewer:** Identifies code issues, maintainability concerns, and adherence to standards.
*   **Test Coverage Checker:** Verifies that all new or changed code is covered by tests.
*   **GitHub Comment Writer:** Generates comments for GitHub pull requests.

## Contributing

Contributions are welcome! Please submit a pull request with your changes.

> Readme has been updated by Codewarden