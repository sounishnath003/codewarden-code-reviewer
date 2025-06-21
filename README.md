# Codewarden - AI Code Reviewer Agent

Your AI-Powered Code Quality Assistant. A code reviewer tool which will run a cli or in github actions and generate the code quality, improvements, and bugs using AI power techniques. 'finger crossed' 

# Project Structure 
```
    codewarden-code-reviewer/
    ├── .github/
    │   └── workflows/
    │       └── commit-review.yaml
    ├── .gitignore
    ├── .python-version
    ├── codewarden/
    │   ├── ai/
    │   │   ├── agents.py
    │   │   ├── base.py
    │   │   ├── llm.py
    │   │   ├── prompts.py
    │   │   ├── tasks.py
    │   │   └── tools.py
    │   ├── command/
    │   │   ├── cli.py
    │   │   ├── logger.py
    │   │   └── utils.py
    │   ├── core/
    │   │   └── config.py
    │   └── hooks/
    │       └── prehooks.py
    ├── CommitsReview.md
    ├── main.py
    ├── Makefile
    ├── pyproject.toml
    ├── README.md
    ├── sample.config.yaml
    └── uv.lock
```