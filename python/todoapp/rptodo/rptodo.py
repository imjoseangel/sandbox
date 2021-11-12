"""This module provides the RP To-Do model-controller."""
# rptodo/rptodo.py
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Any, Dict, NamedTuple

from rptodo.database import DatabaseHandler


class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int


class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
