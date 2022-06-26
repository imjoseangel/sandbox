#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

library = ctypes.cdll.LoadLibrary('./library.so')
hello_world = library.helloWorld
hello_world()
