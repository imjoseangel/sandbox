#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import pathlib
import re
import shutil
from git import Repo, InvalidGitRepositoryError  # type: ignore

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%d-%b-%y %H:%M:%S",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

projects = ["A", "B", "C"]
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
        project_name = str.upper(os.path.dirname(file_path[0]).split('/')[1])

        logging.info(f'File Path: {file_path}')
        logging.info(f'Project Name: {project_name}')

        return project_name

    except IndexError:
        project_name = str.upper(os.path.dirname(file_path[0]).split('/')[0])

        logging.info(f'File Path: {file_path}')
        logging.info(f'Project Name: {project_name}')

        return project_name


def prepare_target(project_name):

    rmdir(artifacts_dir)

    for project in projects:
        if "IPC" not in project:
            mkdir(f'{artifacts_dir}/{project}')
        else:
            mkdir(
                f'{artifacts_dir}/{project}/{project_name}')


def extract_files(path) -> list:

    uploaded_files = []
    file_path = find_files()

    for file in file_path:
        if path in file:
            uploaded_files.append(file)

    return uploaded_files


if __name__ == '__main__':
    GITPROJECT = find_project()
    prepare_target(GITPROJECT)

    # IPC Files
    FILES = extract_files('/a/')
    PARAMETERS = "parameters.txt"

    for csvitem in FILES:
        if ".csv" in csvitem.lower():
            shutil.copyfile(f'{os.getcwd()}/{csvitem}',
                            f'{artifacts_dir}/A/{GITPROJECT}/{os.path.basename(csvitem)}')
            with open(PARAMETERS, 'a', encoding='utf-8') as parameters:
                parameters.write(f'{(csvitem)}\n')
                parameters.close()

    try:
        shutil.copyfile(f'{os.getcwd()}/{PARAMETERS}',
                        f'{artifacts_dir}/A/{GITPROJECT}/{PARAMETERS}')
    except FileNotFoundError:
        pass

    for manifestitem in FILES:
        if re.match(r'manifest$', manifestitem):
            print(manifestitem)
