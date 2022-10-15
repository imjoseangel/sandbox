#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import git


def find_commit_by_tag(tag):
    repo = git.Repo('.')
    return repo.commit(tag)


def get_git_root() -> str:

    repo = git.Repo(os.path.dirname(os.path.realpath(__file__)),
                    search_parent_directories=True)
    git_root = repo.git.rev_parse("--show-toplevel")
    return git_root


print(get_git_root())
