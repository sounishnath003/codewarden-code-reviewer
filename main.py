import os
from crewai import Crew, CrewOutput
import yaml
import argparse
import logging

from codewarden.ai import agents
from codewarden.ai import tasks
from codewarden.command import logger as cw_logger
from codewarden.core.config import Configuration


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
    comment_agent = agents.GithubCommentAgent(conf)

    workflow = Crew(
        agents=[
            context_agent.agent,
            code_review_agent.agent,
            comment_agent.agent,
        ],
        tasks=[
            tasks.WorkspaceContextTask(context_agent.agent).task,
            tasks.CodeReviewTask(code_review_agent.agent).task,
            tasks.GithubCommentTask(comment_agent.agent).task,
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

    conf.logger.info("result: %s", result)
    conf.logger.info("tokens.usage: %s", result.token_usage)


if __name__ == "__main__":
    cw_logger.init_logger()
    main()
