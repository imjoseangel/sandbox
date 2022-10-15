#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import git


def find_commit_by_tag(tag):
    repo = git.Repo('.')
    return repo.commit(tag)


def find_commit_differences():
    repo = git.Repo(os.path)
    print(repo)


find_commit_differences()
