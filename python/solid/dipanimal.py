#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from abc import ABCMeta, abstractmethod


class Animal():
    __metaclass__ = ABCMeta

    @abstractmethod
    def make_sound(self):
        pass

# `Animal` defines a interface which requires `make_sound` method.


class Lion(Animal):
    def make_sound(self):
        print('Roar!!!')


class Mouse(Animal):
    def make_sound(self):
        print('Squeak!!!')

# Now, the manager support `SuperWorker`...
# In addition, it will support any animal which obeys the interface defined by `Animal`!


class Manager():

    def __init__(self):
        self.animal = None

    def set_animal(self, animal):
        assert isinstance(
            animal, Lion), '`animal` must be of type {}'.format(Lion)

        self.animal = animal

    def manage(self):
        if self.animal is not None:
            self.animal.make_sound()
            # And some complex codes go here....


def main():

    lion = Lion()
    manager = Manager()
    manager.set_animal(lion)
    manager.manage()

    # The following will work!
    mouse = Mouse()
    try:
        manager.set_animal(mouse)
        manager.manage()
    except AssertionError:
        print("manager fails to support mouse....")


if __name__ == "__main__":
    main()
