#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import git


def get_git_root() -> git.Repo:

    repo = git.Repo(os.path.dirname(os.path.realpath(__file__)),
                    search_parent_directories=True)
    git_root = repo.git.rev_parse("--show-toplevel")
    return repo


def diff_commit(repo):
    headcommit = repo.head.commit
    diff = headcommit.diff("HEAD^")
    return diff


repo = get_git_root()

for x in diff_commit(repo):
    print(x)
