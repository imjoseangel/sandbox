#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


DEFAULT_LION_LEG_COUNT = 4
DEFAULT_MOUSE_LEG_COUNT = 4
DEFAULT_SNAKE_LEG_COUNT = 0


class Animal:

    def __init__(self, name: str):
        self.name = name
        self.db = AnimalDB()

    def get_name(self) -> str:
        return self.name

    def make_sound(self):
        pass

    def get_legs_count(self):
        pass

    def get(self, id):
        return self.db.get_animal(id)

    def save(self):
        self.db.save(animal=self)


class AnimalDB:

    def get_animal(self, id) -> Animal:
        pass

    def save(self, animal: Animal):
        pass


class Lion(Animal):
    def make_sound(self):
        return 'Roar!!!'

    def get_legs_count(self):
        return DEFAULT_LION_LEG_COUNT


class Mouse(Animal):
    def make_sound(self):
        return 'Squeak!!!'

    def get_legs_count(self):
        return DEFAULT_MOUSE_LEG_COUNT


class Snake(Animal):
    def make_sound(self):
        return 'Sssss!!!'

    def get_legs_count(self):
        return DEFAULT_SNAKE_LEG_COUNT


def animal_sound(animals: list):
    for animal in animals:
        print(animal.make_sound())


def animal_leg_count(animals: list):
    for animal in animals:
        print(animal.get_legs_count())


def main():

    # Single Responsibility
    animal = Animal('Lion')
    animal.save()

    # Open Closed
    animals = [
        Lion('Lion'),
        Mouse('Mouse'),
        Snake('Python')
    ]

    animal_sound(animals)

    # Liskov Substitution
    animal_leg_count(animals)


if __name__ == '__main__':
    main()
