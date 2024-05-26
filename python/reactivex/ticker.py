#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import reactivex as rx

animals = rx.of("ant", "bee", "cat", "dog", "elk")
ticker = rx.interval(0.5)

combined = rx.zip(animals, ticker)
start = time.time()

combined.subscribe(lambda value: print(
    f"Received {value} {time.time()-start:.3f}"))

time.sleep(3)
