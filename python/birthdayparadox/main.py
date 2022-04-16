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


def main():
    """
    Main function
    """


if __name__ == '__main__':
    main()
