#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class ProcessConfig:
    drop_columns: list
    target: str
    test_size: float
    random_state: int
    shuffle: bool = True


def process(config: ProcessConfig):
    target = config.target
    test_size = config.test_size
    random_state = config.random_state
    ...
