#!/usr/bin/env python
# -*- coding: utf-8 -*-

WORD = "SNAKE"

for guess_num in range(1, 7):
    guess = input(f"\nGuess {guess_num}: ").upper()

    if guess == WORD:
        print("Correct")
        break

    print("Wrong")
