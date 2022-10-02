#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel


def get_content(user):
    """Extract content from user dict."""
    country = user["location"]["country"]
    name = f"{user['name']['first']} {user['name']['last']}"

    return f"[b]{name}[/b]\n[yellow]{country}"


console = Console()

users = json.loads(requests.get(
    "https://randomuser.me/api/?results=30", timeout=30).content).get("results")

user_renderables = [Panel(get_content(user), expand=True) for user in users]
console.print(Columns(user_renderables))
