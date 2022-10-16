#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from git import Repo, InvalidGitRepositoryError  # type: ignore
from rich import print as richprint


def get_git_root() -> Repo:  # type: ignore

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


def prepare_target_directory():
    try:
        shutil.rmtree(os.environ["BUILD_ARTIFACTSTAGINGDIRECTORY"])
    except KeyError as keyerror:
        richprint(f'{keyerror} variable does not exist')
    except FileNotFoundError as filenotfound:
        richprint(f'{filenotfound} directory does not exist')


prepare_target_directory()

try:
    richprint(diff_commit(get_git_root()))
except AttributeError as attributeerror:
    richprint(attributeerror)

for item in diff_commit(get_git_root()):
    if "main" in item:
        richprint(item)
