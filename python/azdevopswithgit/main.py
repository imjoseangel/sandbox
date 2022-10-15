#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from git import Repo


def get_git_root() -> Repo:

    gitrepo = Repo(os.path.dirname(os.path.realpath(__file__)),
                   search_parent_directories=True)
    gitroot = gitrepo.git.rev_parse("--show-toplevel")
    return gitrepo


def diff_commit(gitrepo):
    headcommit = gitrepo.head.commit
    diff = headcommit.diff("HEAD~1", name_only=True)
    return diff


repo = get_git_root()

print(diff_commit(repo))
