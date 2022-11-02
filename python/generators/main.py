#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pp
from timeit import timeit
import matplotlib.pyplot as plt

TIMEIT_TIMES = 100
LIST_SIZE = 500
POSITION_INCREMENT = 10


def build_list(size, fill, value, at_position):
    return [value if i == at_position else fill for i in range(size)]


def find_match_loop(iterable):
    for value in iterable:
        if value["population"] > 50:
            return value
    return None


def find_match_gen(iterable):
    return next(
        (value for value in iterable if value["population"] > 50),
        None
    )


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

looping_times = []
generator_times = []
positions = []

for position in range(0, LIST_SIZE, POSITION_INCREMENT):
    print(
        f"Progress {position / LIST_SIZE:.0%}",
        end=f"{3 * ' '}\r",  # Clear previous characters and reset cursor
    )

    positions.append(position)

    list_to_search = build_list(
        LIST_SIZE,
        {"country": "Nowhere", "population": 10},
        {"country": "Atlantis", "population": 100},
        position,
    )

    looping_times.append(
        timeit(
            "find_match_loop(list_to_search)",
            globals=globals(),
            number=TIMEIT_TIMES,
        )
    )
    generator_times.append(
        timeit(
            "find_match_gen(list_to_search)",
            globals=globals(),
            number=TIMEIT_TIMES,
        )
    )

print("Progress 100%")

fig, ax = plt.subplots()

plot = ax.plot(positions, looping_times, label="loop")
plot = ax.plot(positions, generator_times, label="generator")

plt.xlim([0, LIST_SIZE])
plt.ylim([0, max(max(looping_times), max(generator_times))])

plt.xlabel("Index of element to be found")
plt.ylabel(f"Time in seconds to find element {TIMEIT_TIMES:,} times")
plt.title("Raw Time to Find First Match")
plt.legend()

plt.show()

# Ratio

looping_ratio = [loop / loop for loop in looping_times]
generator_ratio = [
    gen / loop for gen, loop in zip(generator_times, looping_times)
]

fig, ax = plt.subplots()

plot = ax.plot(positions, looping_ratio, label="loop")
plot = ax.plot(positions, generator_ratio, label="generator")

plt.xlim([0, LIST_SIZE])
plt.ylim([0, max(max(looping_ratio), max(generator_ratio))])

plt.xlabel("Index of element to be found")
plt.ylabel("Speed to find element, relative to loop")
plt.title("Relative Speed to Find First Match")
plt.legend()

plt.show()
