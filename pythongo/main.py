#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

library = ctypes.cdll.LoadLibrary('./library.so')
hello_world = library.helloWorld
hello_world()


hello = library.hello
hello.argtypes = [ctypes.c_char_p]
hello("everyone".encode('utf-8'))
