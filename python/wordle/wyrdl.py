#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import random
from string import ascii_letters
from rich.console import Console
from rich.theme import Theme

console = Console(width=40)
console = Console(width=40, theme=Theme({"warning": "red on yellow"}))


def get_random_word(wordlist):
    """Get a random five-letter word from a list of strings.

    ## Example:

    >>> get_random_word(["snake", "worm", "it'll"])
    'SNAKE'
    """

    words = [
        word.upper()
        for word in wordlist
        if len(word) == 5 and all(letter in ascii_letters for letter in word)
    ]
    return random.choice(words)


def show_guesses(guesses, word):
    for guess in guesses:
        styled_guess = []
        for letter, correct in zip(guess, word):
            if letter == correct:
                style = "bold white on green"
            elif letter in word:
                style = "bold white on yellow"
            elif letter in ascii_letters:
                style = "white on #666666"
            else:
                style = "dim"
            styled_guess.append(f"[{style}]{letter}[/]")

        console.print("".join(styled_guess), justify="center")


def game_over(word):
    print(f"The word was {word}")


def refresh_page(headline):
    console.clear()
    console.rule(f"[bold blue]:leafy_green: {headline} :leafy_green:[/]\n")


def main():
    # Pre-process
    words = pathlib.Path(__file__).parent / "wordlist.txt"
    word = get_random_word(words.read_text(encoding="utf-8").split("\n"))
    guesses = ["_" * 5] * 6

    # Process (main loop)
    for idx in range(6):
        refresh_page(headline=f"Guess {idx + 1}")
        show_guesses(guesses, word)

        guesses[idx] = input("\nGuess word: ").upper()
        if guesses[idx] == word:
            break

    # Post-process
    else:
        game_over(word=word)


if __name__ == '__main__':
    main()
