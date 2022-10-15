#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from git import Repo


def get_git_root() -> Repo:

    gitrepo = Repo(os.path.dirname(os.path.realpath(__file__)),
                   search_parent_directories=True)
    return gitrepo


def get_git_name() -> str:
    return get_git_root().git.rev_parse("--show-toplevel")


def diff_commit(gitrepo):
    diff = gitrepo.git.diff("HEAD^", name_only=True)
    return diff


print(diff_commit(get_git_root()))
