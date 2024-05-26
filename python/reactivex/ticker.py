#!/usr/bin/env python
# -*- coding: utf-8 -*-

from timeit import default_timer as timer
import time
import reactivex as rx

animals = rx.of("ant", "bee", "cat", "dog", "elk")
ticker = rx.interval(0.5)

combined = rx.zip(animals, ticker)
start = timer()

combined.subscribe(lambda value: print(
    f"Received {value} {timer()-start:.3f}"))

time.sleep(3)
