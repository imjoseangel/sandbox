#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from git import Repo, InvalidGitRepositoryError
from rich.console import Console


console = Console()


def get_git_root() -> Repo:

    try:
        gitrepo = Repo(os.getcwd(),
                       search_parent_directories=True)
        return gitrepo
    except InvalidGitRepositoryError:
        pass


def get_git_name() -> str:
    return get_git_root().git.rev_parse("--show-toplevel")


def diff_commit(gitrepo):
    diff = gitrepo.git.diff("HEAD^..HEAD", name_only=True, diff_filter="AM")
    return diff


try:
    print(diff_commit(get_git_root()))
except AttributeError as attributeerror:
    console.log(attributeerror)
