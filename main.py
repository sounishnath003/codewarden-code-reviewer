import datetime
import os
from crewai import Crew, CrewOutput
import yaml
import argparse
import logging

from codewarden.ai import agents
from codewarden.ai import tasks
from codewarden.command import logger as cw_logger
from codewarden.core.config import Configuration


def update_readme_with_commit_review(result: CrewOutput) -> None:
    # Write the code review result to README.md
    readme_path = "CommitsReview.md"
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as file:
            readme_content = file.read()
    else:
        with open(readme_path, "w+", encoding="utf-8") as file:
            file.write("")
            readme_content = ""
            file.close()

    # Find and replace the code review section
    code_review_start = "## Code Review"
    code_review_end = "## "

    # Extract content before and after the code review section
    if code_review_start in readme_content:
        before_section = readme_content.split(code_review_start)[0]
        after_sections = readme_content.split(code_review_start)[1:]

        if after_sections:
            # Find the next section marker
            remaining_content = after_sections[0]
            if code_review_end in remaining_content:
                after_section = (
                    code_review_end + remaining_content.split(code_review_end, 1)[1]
                )
            else:
                after_section = ""
        else:
            after_section = ""
    else:
        # If no code review section exists, add it before the last section
        sections = readme_content.split("## ")
        if len(sections) > 1:
            before_section = "## ".join(sections[:-1])
            after_section = "## " + sections[-1]
        else:
            before_section = readme_content
            after_section = ""

    # Create new code review content
    new_code_review_section = f"""## Code Review

### Latest Code Review Results
- *Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
- *Token usage: {result.token_usage}*

{result.__str__().replace("```markdown", "")}

---
"""

    # Write updated README
    updated_readme = before_section + new_code_review_section + after_section
    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(updated_readme)

    logging.info("Updated CommitsReview.md with latest code review results")


def init_config() -> Configuration | None:
    """parses the runtime --config file and return the Configuration instance for the project as defined"""
    # create a argument parser
    parser = argparse.ArgumentParser("codewarden")
    # add the arguments
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="provide the config yaml file for your environment",
    )
    # parse the pipeline args and unknown args
    opts, pipeline_opts = parser.parse_known_args()
    conf = None
    # try to open config and read the yaml and parse it
    with open(opts.config, "r+", encoding="utf-8") as file:
        logging.info("trying to read config file %s", opts.config)
        config = yaml.safe_load(file)
        logging.info("config %s", config)
        conf = Configuration(**config)
        file.close()

    return conf


def main():
    # initialize the configuration for the project
    conf = init_config()
    if not conf:
        raise Exception("no configuration provided")

    # Agents:
    context_agent = agents.WorkspaceContextAgent(conf=conf)
    code_review_agent = agents.CodeReviewAgent(conf)
    test_agent = agents.CodeTestAgent(conf)
    comment_agent = agents.GithubCommentAgent(conf)

    workflow = Crew(
        agents=[
            context_agent.agent,
            code_review_agent.agent,
            # test_agent.agent,
            # comment_agent.agent,
        ],
        tasks=[
            tasks.WorkspaceContextTask(context_agent.agent).task,
            tasks.CodeReviewTask(code_review_agent.agent).task,
            # tasks.CodeTestTask(test_agent.agent).task,
            # tasks.GithubCommentTask(comment_agent.agent).task,
        ],
        verbose=True,
    )

    result = workflow.kickoff(
        inputs={
            "directory_path": os.path.join(os.getcwd()),
            "exclude_files": [
                ":(exclude)docs/",
                ":(exclude)uv.lock",
                ":(exclude)**/*.md",
                ":(exclude)package-lock.json",
            ],
        }
    )

    update_readme_with_commit_review(result)
    conf.logger.info("tokens.usage: %s", result.token_usage)


if __name__ == "__main__":
    cw_logger.init_logger()
    main()
