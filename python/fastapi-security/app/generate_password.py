#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bcrypt
from rich import prompt, print as rprint


def main():

    password = prompt.Prompt.ask(
        "Enter the [bold yellow]password[/bold yellow] ", password=True)
    assert password

    # converting password to array of bytes
    password_encoded = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    password_hash = bcrypt.hashpw(password_encoded, salt)

    rprint(password_hash.decode("utf-8"))


if __name__ == '__main__':
    main()
