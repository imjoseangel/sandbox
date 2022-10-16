#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import pathlib
import shutil
from git import Repo, InvalidGitRepositoryError  # type: ignore

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%d-%b-%y %H:%M:%S",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
        logging.error(f'{keyerror} variable does not exist')
    except FileNotFoundError as filenotfound:
        logging.error(f'{filenotfound} directory does not exist')


def mkdir(path):
    try:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    except FileExistsError as fileexist:
        logging.error(f'{fileexist} directory already exists')
    except FileNotFoundError as filenotfound:
        logging.error(f'{filenotfound} directory does not exist')


def rmfile(path):
    try:
        os.remove(path)
    except FileNotFoundError as filenotfound:
        logging.error(f'{filenotfound} file does not exist')


def find_files() -> list:
    file_path = diff_commit(get_git_root())

    return file_path


def find_project() -> str:

    file_path = find_files()

    try:
        project_name = str.upper(os.path.dirname(file_path[0]).split('/')[0])

        logging.info(f'File Path: {file_path}')
        logging.info(f'Project Name: {project_name}')

        return project_name

    except IndexError as indexerror:
        logging.error(f'{indexerror} No file found')


def prepare_target():

    rmdir(artifacts_dir)

    project_name = find_project()

    for project in projects:
        if "IPC" not in project:
            mkdir(f'{artifacts_dir}/{project}')
        else:
            mkdir(
                f'{artifacts_dir}/{project}/{project_name}')


def extract_files(path):

    uploaded_files = []
    file_path = find_files()

    for file in file_path:
        if path in file:
            uploaded_files.append(file)

    return uploaded_files


if __name__ == '__main__':
    prepare_target()
    gitproject = find_project()

    # IPC Files
    files = extract_files('/ipc/')
    parameters_file = "parameter_files.txt"

    rmfile(parameters_file)
    for item in files:
        if ".csv" in item.lower():
            shutil.copyfile(f'{os.getcwd()}/ipc/{os.path.basename(item)}',
                            f'{artifacts_dir}/IPC/{gitproject}/{os.path.basename(item)}')
            with open(parameters_file, 'a', encoding='utf-8') as parameters:
                parameters.write(f'{(item)}\n')
                parameters.close()

# try:
#     richprint(diff_commit(get_git_root()))
# except AttributeError as attributeerror:
#     richprint(attributeerror)

# for item in diff_commit(get_git_root()):
#     if "main" in item:
#         richprint(item)
