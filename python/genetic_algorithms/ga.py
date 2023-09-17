#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import numpy as np
import matplotlib.pyplot as plt


def main():
    img = np.random.randint(2, size=(15, 15))
    plt.imshow(img, cmap=plt.cm.winter)
    plt.show()


if __name__ == '__main__':
    main()
