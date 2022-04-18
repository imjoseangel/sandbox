#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Birthday Paradox Simulation
Explore the surprising probabilities of the "Birthday Paradox".
More info at https://en.wikipedia.org/wiki/Birthday_problem"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import datetime
import random


def getBirthdays(numberOfBirthdays):
    """Returns a list of number random date objects for birthdays."""
    birthdays = []
    for _ in range(numberOfBirthdays):
        # The year is unimportant for our simulation, as long as all
        # birthdays are in the same year.
        startOfYear = datetime.date(2001, 1, 1)

        # Generate a random number of days between 1 and 365.
        randomNumberOfDays = datetime.timedelta(random.randint(0, 364))
        birthday = startOfYear + randomNumberOfDays
        birthdays.append(birthday)

    return birthdays


def getMatch(birthdays):
    """Returns the date object of a birthday that occurs more than once
    in the list of birthdays."""

    if len(birthdays) == len(set(birthdays)):
        return None  # All birthdays are unique, so return None.

    # Compare each birthday to every other birthday.
    for a, birthdayA in enumerate(birthdays):
        for b, birthdayB in enumerate(birthdays[a + 1:]):
            if birthdayA == birthdayB:
                return birthdayA  # Return the matching birthday.


def main():
    """
    Birthday Paradox, by Al Sweigart al@inventwithpython.com

    The birthday paradox shows us that in a group of N people, the odds
    that two of them have matching birthdays is surprisingly large.
    This program does a Monte Carlo simulation (that is, repeated random
    simulations) to explore this concept.

    (It's not actually a paradox, it's just a surprising result.)
    """

    # Display the intro:
    print('''Birthday Paradox, by Al Sweigart al@inventwithpython.com

    The birthday paradox shows us that in a group of N people, the odds
    that two of them have matching birthdays is surprisingly large.
    This program does a Monte Carlo simulation (that is, repeated random
    simulations) to explore this concept.

    (It's not actually a paradox, it's just a surprising result.)
    ''')

    # Set up a tuple of month names in order:
    MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

    while True:
        print('How many birthdays do you want to simulate? (1-100)')
        response = input('> ')
        if response.isdigit() and 1 <= int(response) <= 100:
            numBdays = int(response)
            break  # User has entered a valid number of birthdays to simulate.
    print('\n')

    # Run through 100,000 simulations:
    print('Generating', numBdays, 'random birthdays 100,000 times...')
    input('Press Enter to begin...')

    print('Let\'s run another 100,000 simulations.')
    simMatch = 0  # How many simulations have a matching birthday.
    for i in range(100000):
        # Report on the progress every 10000 simulations:
        if i % 10000 == 0:
            print('Simulation', i, 'of 100,000...')
        birthdays = getBirthdays(numBdays)
        if getMatch(birthdays) is not None:
            simMatch += 1
    print('100,000 simulations complete.')

    # Display the results:
    probability = round(simMatch / 100000 * 100, 2)

    print('Out of 100,000 simulations of', numBDays, 'people, there was a')
    print('matching birthday in that group', simMatch, 'times. This means')
    print('that', numBDays, 'people have a', probability, '% chance of')
    print('having a matching birthday in their group.')
    print('That\'s probably more than you would think!')


if __name__ == '__main__':
    main()
