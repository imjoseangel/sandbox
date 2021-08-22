#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


class Person:

    def __init__(self, firstName, lastName, idNumber):
        self.firstName = firstName
        self.lastName = lastName
        self.idNumber = idNumber

    def printPerson(self):
        print("Name:", self.lastName + ",", self.firstName)
        print("ID:", self.idNumber)


class Student(Person):

    def __init__(self, firstName, lastName, idNumber, scores):

        super().__init__(firstName, lastName, idNumber)
        self.scores = scores

    #   Class Constructor
    #
    #   Parameters:
    #   firstName - A string denoting the Person's first name.
    #   lastName - A string denoting the Person's last name.
    #   id - An integer denoting the Person's ID number.
    #   scores - An array of integers denoting the Person's test scores.
    #
    # Write your constructor here

    #   Function Name: calculate
    #   Return: A character denoting the grade.
    #
    # Write your function here

    def calculate(self):

        grade = sum(self.scores) / len(self.scores)

        scale = {90 <= grade <= 100: "O", 80 <=
                 grade < 90: "E", 70 <= grade < 80: "A",
                 55 <= grade < 70: "P", 40 <= grade < 55: "D",
                 grade < 40: "T"}

        return scale.get(True)


def main():

    firstName = "Memelli"
    lastName = "Heraldo"
    idNum = "8135627"
    scores = [100, 80]
    s = Student(firstName, lastName, idNum, scores)
    s.printPerson()
    print("Grade:", s.calculate())


if __name__ == '__main__':
    main()
