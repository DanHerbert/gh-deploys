import os
import logging
from dataclasses import dataclass

import yaml

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_PATH, "../config/", "config.yaml")


@dataclass
class Command:
    def __init__(self, cmd, user):
        self.cmd = cmd
        self.user = user


@dataclass
class Project:
    def __init__(self, repo_name, repo_path, deploy_branch, commands):
        self.repo_name = repo_name
        self.repo_path = repo_path
        self.deploy_branch = deploy_branch
        self.commands = commands


@dataclass
class Config:

    def __init__(  # pylint: disable=too-many-arguments
        self, root_path, log_level, secret, debug_listen_port, debug_mode, projects
    ):
        self.root_path = root_path
        self.log_level = log_level
        self.secret = secret
        self.debug_listen_port = debug_listen_port
        self.debug_mode = debug_mode
        self.projects = projects


def get_config():
    """Gets the config object from disk."""
    with open(CONFIG_PATH, mode="rt", encoding="utf-8") as file_handle:
        conf_dict = yaml.safe_load(file_handle)
        projects = []
        for project_dict in conf_dict["projects"]:
            commands = []
            for command_dict in project_dict["commands"]:
                commands.append(Command(command_dict["cmd"], command_dict["user"]))
            projects.append(
                Project(
                    project_dict["repo_name"],
                    project_dict.get("repo_path"),
                    project_dict["deploy_branch"],
                    commands,
                )
            )
        return Config(
            conf_dict["root_path"],
            logging.getLevelName(conf_dict["log_level"]),
            conf_dict["secret"],
            conf_dict["debug_listen_port"],
            conf_dict["debug_mode"],
            projects,
        )
