#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import pandas as pd


# Function to add
def add(a, b, c):
    return a + b + c


def main():

    # Create dict with 3 fields each
    data = {
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]
    }

    # Convert the dict into dataframe
    df = pd.DataFrame(data)
    print("Original Dataframe:\n", df)

    df['ADD'] = df.apply(lambda row: add(row['A'], row['B'], row['C']), axis=1)

    print('\nAfter Applying Function: ')

    # printing the new dataframe
    print(df)


if __name__ == '__main__':
    main()
