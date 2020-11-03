#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------

# Update the VARIANT arg in devcontainer.json to pick a Python version: 3, 3.8, 3.7, 3.6
# To fully customize the contents of this image, use the following Dockerfile instead:
# https://github.com/microsoft/vscode-dev-containers/tree/v0.109.0/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT=8
FROM imjoseangel/debian:${VARIANT}

# This Dockerfile adds a non-root user with sudo access. Use the "remoteUser"
# property in devcontainer.json to use it. On Linux, the container user's GID/UIDs
# will be updated to match your local UID/GID (when using the dockerFile property).
# See https://aka.ms/vscode-remote/containers/non-root-user for details.
ARG USERNAME=ansible
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG ANSIBLE_PASS=.ansible_password

# Uncomment the following COPY line and the corresponding lines in the `RUN` command if you wish to
# include your requirements in the image itself. Only do this if your requirements rarely change.
COPY requirements.txt secrets/* /tmp/pip-tmp/

# Set to false to skip installing zsh and Oh My ZSH!
ARG INSTALL_ZSH="false"

# Location and expected SHA for common setup script - SHA generated on release
ARG COMMON_SCRIPT_SOURCE="common-debian.sh"
ARG COMMON_SCRIPT_SHA="dev-mode"

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

ADD scripts/${COMMON_SCRIPT_SOURCE} /tmp/common-setup.sh
# Configure apt and install packages
RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog wget ca-certificates 2>&1 \
    #
    # Verify git, common tools / libs installed, add/modify non-root user, optionally install zsh
    && if [ "$COMMON_SCRIPT_SHA" != "dev-mode" ]; then echo "$COMMON_SCRIPT_SHA /tmp/common-setup.sh" | sha256sum -c - ; fi \
    && /bin/bash /tmp/common-setup.sh "$INSTALL_ZSH" "$USERNAME" "$USER_UID" "$USER_GID" \
    && rm /tmp/common-setup.sh \
    #
    # Update Python environment based on requirements.txt
    && pip3 --disable-pip-version-check --no-cache-dir install --upgrade -r /tmp/pip-tmp/requirements.txt \
    && if [ -f /tmp/pip-tmp/"${ANSIBLE_PASS}" ]; then cp /tmp/pip-tmp/"${ANSIBLE_PASS}" /home/"${USERNAME}"; fi \
    && rm -rf /tmp/pip-tmp \
    #
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

# [Optional] Allow the vscode user to pip install globally w/o sudo
ENV PIP_TARGET=/usr/local/pip-global
ENV PYTHONPATH=${PIP_TARGET}:${PYTHONPATH}
ENV PATH=${PIP_TARGET}/bin:${PATH}
RUN mkdir -p ${PIP_TARGET} \
    && chown ansible:root ${PIP_TARGET} \
    && export SNIPPET="if [ \"\$(stat -c '%U' ${PIP_TARGET})\" != \"ansible\" ]; then chown -R ansible:root ${PIP_TARGET}; fi" \
    && echo "$SNIPPET" | tee -a /root/.bashrc >> /home/ansible/.bashrc \
    && echo "$SNIPPET" | tee -a /root/.zshrc >> /home/ansible/.zshrc
