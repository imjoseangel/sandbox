#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from git import Repo
from rich.console import Console


console = Console()


def get_git_root() -> Repo:

    gitrepo = Repo(os.path.dirname(os.path.realpath(__file__)),
                   search_parent_directories=True)
    return gitrepo


def get_git_name() -> str:
    return get_git_root().git.rev_parse("--show-toplevel")


def diff_commit(gitrepo):
    diff = gitrepo.git.diff("HEAD^", name_only=True, diff_filter="AM")
    return diff


console.log(diff_commit(get_git_root()))
