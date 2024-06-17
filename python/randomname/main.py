#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import requests

name = requests.get(
    'https://randomuser.me/api/1.4?results=100', timeout=10).json()


# print(json.dumps(name, indent=4, sort_keys=True))

def names():
    for i in name["results"]:
        yield i["name"]["first"]


def lastnames():
    for i in name["results"]:
        yield i["name"]["last"]


def cities():
    for i in name["results"]:
        yield i["location"]["city"]


def ages():
    for i in name["results"]:
        yield i["dob"]["age"]


first_names = list(names())
last_names = list(lastnames())
city = list(cities())
age = list(ages())

print(first_names, last_names, city, age)

for item in zip(first_names, last_names, age, city):

    sentence = f"Hi {item[0]}, this is {item[1]}! I'm {item[2]} years old and {random.choice(
        ['loving life', 'thriving', 'enjoying', 'living it up', 'chilling'])} in {item[3]}."

    print(sentence)
