#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from git import Repo, InvalidGitRepositoryError
from rich import print


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
    return diff.split()


try:
    print(diff_commit(get_git_root()))
except AttributeError as attributeerror:
    print(attributeerror)

for item in diff_commit(get_git_root()):
    if "main" in item:
        print(item)
