#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def trapezoidal_rule(f, a, b, n):
    x = np.linspace(a, b, n+1)
    y = f(x)
    h = (b - a) / n
    integral = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    return integral


def main():
    # Example usage
    def f(x): return np.sin(x)

    a, b, n = 0, np.pi, 1000
    result = trapezoidal_rule(f, a, b, n)
    print(f"Trapezoidal Rule Result: {result}")


if __name__ == '__main__':
    main()
