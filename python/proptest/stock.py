#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hypothesis import given
from hypothesis import strategies as some


class Warehouse:
    def __init__(self, stock):
        self.stock = stock

    def in_stock(self, item_name, quantity):
        return (item_name in self.stock) and (self.stock[item_name] >= quantity)

    def take_from_stock(self, item_name, quantity):
        if quantity <= self.stock[item_name]:
            self.stock[item_name] -= quantity
        else:
            raise Exception(f"Oversold {item_name}")

    def stock_count(self, item_name):
        return self.stock[item_name]


def test_wharehouse():
    wh = Warehouse({"shoes": 10, "hats": 2, "umbrellas": 0})
    assert wh.in_stock("shoes", 10)
    assert wh.in_stock("hats", 2)
    assert not wh.in_stock("umbrellas", 1)

    wh.take_from_stock("shoes", 2)
    assert wh.in_stock("shoes", 8)
    wh.take_from_stock("hats", 2)
    assert not wh.in_stock("hats", 1)


def order(warehouse, item, quantity):
    if warehouse.in_stock(item, quantity):
        warehouse.take_from_stock(item, quantity)
        return ("ok", item, quantity)
    else:
        return ("not available", item, quantity)


def test_order_in_stock():
    wh = Warehouse({"shoes": 10, "hats": 2, "umbrellas": 0})
    status, item, quantity = order(wh, "hats", 1)
    assert status == "ok"
    assert item == "hats"
    assert quantity == 1
    assert wh.stock_count("hats") == 1


def test_order_not_in_stock():
    wh = Warehouse({"shoes": 10, "hats": 2, "umbrellas": 0})
    status, item, quantity = order(wh, "umbrellas", 1)
    assert status == "not available"
    assert item == "umbrellas"
    assert quantity == 1
    assert wh.stock_count("umbrellas") == 0


def test_order_unknown_item():
    wh = Warehouse({"shoes": 10, "hats": 2, "umbrellas": 0})
    status, item, quantity = order(wh, "bagel", 1)
    assert status == "not available"
    assert item == "bagel"
    assert quantity == 1


@given(item=some.sampled_from(["shoes", "hats"]),
       quantity=some.integers(min_value=1, max_value=4))
def test_stock_level_plus_quantity_equals_original_stock_level(item, quantity):
    wh = Warehouse({"shoes": 10, "hats": 2, "umbrellas": 0})
    initial_stock_level = wh.stock_count(item)
    (status, item, quantity) = order(wh, item, quantity)
    if status == "ok":
        assert wh.stock_count(item) + quantity == initial_stock_level


@given(item=some.sampled_from(["shoes", "hats"]), quantity=some.integers())
def test_stock_level_plus_any_quantity(item, quantity):
    wh = Warehouse({"shoes": 10, "hats": 2, "umbrellas": 0})
    initial_stock_level = wh.stock_count(item)
    (status, item, quantity) = order(wh, item, quantity)
    if status == "ok":
        assert wh.stock_count(item) + quantity == initial_stock_level
