#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

library = ctypes.cdll.LoadLibrary('./library.so')
hello_world = library.helloWorld
hello_world()


hello = library.hello
hello.argtypes = [ctypes.c_char_p]
hello("everyone".encode('utf-8'))

farewell = library.farewell
farewell.restype = ctypes.c_void_p

# this is a pointer to our string
farewell_output = farewell()

# we dereference the pointer to a byte array
farewell_bytes = ctypes.string_at(farewell_output)

# convert our byte array to a string
farewell_string = farewell_bytes.decode('utf-8')

print(farewell_output, farewell_bytes, farewell_string)
