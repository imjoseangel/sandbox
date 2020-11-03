#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class Animal:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_legs_lion(self):
        raise NotImplementedError

    @abstractmethod
    def get_legs_mouse(self):
        raise NotImplementedError

    @abstractmethod
    def get_legs_snake(self):
        raise NotImplementedError


class Lion(Animal):

    def get_legs_lion(self):
        print(4)

    def get_legs_mouse(self):
        print(4)

    def get_legs_snake(self):
        print(0)


class Mouse(Animal):

    def get_legs_lion(self):
        print(4)

    def get_legs_mouse(self):
        print(4)

    def get_legs_snake(self):
        print(0)


class Snake(Animal):

    def get_legs_lion(self):
        print(4)

    def get_legs_mouse(self):
        print(4)

    def get_legs_snake(self):
        print(0)


class Manager():

    def __init__(self):
        self.animal = None

    def set_animal(self, animal):
        assert isinstance(
            animal, Animal), "`animal` must be of type {}".format(Animal)

        self.animal = animal

    def get_legs_lion(self):
        self.animal.get_legs_lion()

    def get_legs_mouse(self):
        self.animal.get_legs_mouse()

    def get_legs_snake(self):
        self.animal.get_legs_snake()


def main():

    manager = Manager()
    manager.set_animal(Lion())
    manager.get_legs_lion()

    manager.set_animal(Mouse())
    manager.get_legs_mouse()

    manager.set_animal(Snake())
    manager.get_legs_snake()


if __name__ == '__main__':
    main()
