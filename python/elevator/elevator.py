#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABC, abstractmethod

# The Elevator class is the context. It should be initiated with a default state.


class Elevator:

    _state = None

    def __init__(self, state: State) -> None:
        self.setElevator(state)

    # method to change the state of the object
    def setElevator(self, state: State) -> None:

        self._state = state
        self._state.elevator = self

    def presentState(self):
        print(f"Elevator is in {type(self._state).__name__}")

    # the methods for executing the elevator functionality. These depends on the
    # current state of the object.
    def pushDownBtn(self):
        self._state.pushDownBtn()

    def pushUpBtn(self):
        self._state.pushUpBtn()

    # if both the buttons are pushed at a time, nothing should happen
    def pushUpAndDownBtns(self) -> None:
        print("Oops.. you should press one button at a time")

    # if no button was pushed, it should just wait open for guests
    def noBtnPushed(self) -> None:
        print("Press any button. Up or Down")

# The common state interface for all the states


class State(ABC):
    @property
    def elevator(self) -> Elevator:
        return self._elevator

    @elevator.setter
    def elevator(self, elevator: Elevator) -> None:
        self._elevator = elevator

    @abstractmethod
    def pushDownBtn(self) -> None:
        pass

    @abstractmethod
    def pushUpBtn(self) -> None:
        pass


# The concrete states
# We have two states of the elevator: when it is on the First floor and the Second floor
class firstFloor(State):

    # If the down button is pushed when it is already on the first floor, nothing should happen
    def pushDownBtn(self) -> None:
        print("Already in the bottom floor")

    # if up button is pushed, move upwards then it changes its state to second floor.
    def pushUpBtn(self) -> None:
        print("Elevator moving upward one floor.")
        self.elevator.setElevator(secondFloor())


class secondFloor(State):

    # if down button is pushed it should move one floor down and open the door
    def pushDownBtn(self) -> None:
        print("Elevator moving down a floor...")
        self.elevator.setElevator(firstFloor())

    # if up button is pushed nothing should happen
    def pushUpBtn(self) -> None:
        print("Already in the top floor")


if __name__ == "__main__":
    # The client code.

    myElevator = Elevator(firstFloor())
    myElevator.presentState()

    # Up button is pushed
    myElevator.pushUpBtn()

    myElevator.presentState()
