#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pp


def build_list(size, fill, value, at_position):
    return [value if i == at_position else fill for i in range(size)]


countries = [
    {"country": "Austria", "population": 8_840_521},
    {"country": "Canada", "population": 37_057_765},
    {"country": "Cuba", "population": 11_338_138},
    {"country": "Dominican Republic", "population": 10_627_165},
    {"country": "Germany", "population": 82_905_782},
    {"country": "Norway", "population": 5_311_916},
    {"country": "Philippines", "population": 106_651_922},
    {"country": "Poland", "population": 37_974_750},
    {"country": "Scotland", "population": 5_424_800},
    {"country": "United States", "population": 326_687_501},
]

for country in countries:
    if country["population"] > 100_000_000:
        print(country["country"])
        break

for country in countries:
    match country:
        case {"population": population} if population > 100_000_000:
            print(country["country"])
            break

pp(
    build_list(
        size=10,
        fill={"country": "Nowhere", "population": 10},
        value={"country": "Atlantis", "population": 100},
        at_position=5,
    )
)
