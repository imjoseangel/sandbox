FROM fedora:latest

LABEL maintainer="@imjoseangel"

RUN dnf -y update \
    && dnf -y install \
    python3-pip procps && \
    dnf clean all

RUN pip3 install --upgrade \
    setuptools \
    pip

ADD requirements.txt /requirements.txt
RUN pip3 install --upgrade -r /requirements.txt

RUN groupadd -g 1001 ansible && \
    useradd -r -u 1001 -g ansible ansible

RUN mkdir /home/ansible
RUN chown -R ansible:ansible /home/ansible

USER ansible

WORKDIR /home/ansible
