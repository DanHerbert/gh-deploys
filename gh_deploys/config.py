import os
import logging
from dataclasses import dataclass

import yaml

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_PATH, '../config/', 'config.yaml')

# TODO Define config class and parse into it.
# TODO Define project class.

@dataclass
class Project:
    def __init__(self, repo_name, deploy_branch, command):
        self.repo_name = repo_name
        self.deploy_branch = deploy_branch
        self.command = command

@dataclass
class Config:
    def __init__(self, root_path, log_level, secret, projects):
        self.root_path = root_path
        self.log_level = log_level
        self.secret = secret
        self.projects = projects

def get_config():
    """Gets the config object from disk."""
    with open(CONFIG_PATH, mode='rt', encoding='utf-8') as file_handle:
        conf_dict = yaml.safe_load(file_handle)
        projects = []
        for project_dict in conf_dict["projects"]:
            projects.append(Project(
                    project_dict["repo_name"],
                    project_dict["deploy_branch"],
                    project_dict["command"]))
        return Config(
                conf_dict["root_path"],
                logging.getLevelName(conf_dict["log_level"]),
                conf_dict["secret"],
                projects)
