#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib
import shutil
from git import Repo, InvalidGitRepositoryError  # type: ignore
from rich import print as richprint

projects = ["IPC", "DB2", "MSTR"]
artifacts_dir = os.environ["BUILD_ARTIFACTSTAGINGDIRECTORY"]


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


def rmdir(path):
    try:
        shutil.rmtree(path)
    except KeyError as keyerror:
        richprint(f'{keyerror} variable does not exist')
    except FileNotFoundError as filenotfound:
        richprint(f'{filenotfound} directory does not exist')


def mkdir(path):
    try:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    except FileExistsError as fileexist:
        richprint(f'{fileexist} directory already exists')
    except FileNotFoundError as filenotfound:
        richprint(f'{filenotfound} directory does not exist')


def rmfile(path):
    try:
        os.remove(path)
    except FileNotFoundError as filenotfound:
        richprint(f'{filenotfound} file does not exist')


def prepare_target():

    rmdir(artifacts_dir)

    file_path = diff_commit(get_git_root())
    project_name = str.upper(os.path.dirname(file_path[0]).split('/')[0])

    richprint(f'File Path: {file_path}')
    richprint(f'Project Name: {project_name}')

    for item in projects:
        if "IPC" not in item:
            mkdir(f'{artifacts_dir}/{item}')
        else:
            mkdir(
                f'{artifacts_dir}/{item}/{project_name}')


def extract_parameter_files():
    rmfile('parameter_files.txt')


if __name__ == '__main__':
    prepare_target()
    extract_parameter_files()
    print(get_git_name())


# try:
#     richprint(diff_commit(get_git_root()))
# except AttributeError as attributeerror:
#     richprint(attributeerror)

# for item in diff_commit(get_git_root()):
#     if "main" in item:
#         richprint(item)
