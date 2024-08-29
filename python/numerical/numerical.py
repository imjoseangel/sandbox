#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# From https://medium.com/pythoneers/advanced-numerical-methods-in-python-2822777e4934

import numpy as np


def trapezoidal_rule(f, a, b, n):
    x = np.linspace(a, b, n+1)
    y = f(x)
    h = (b - a) / n
    integral = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    return integral


def simpsons_rule(f, a, b, n):
    x = np.linspace(a, b, n+1)
    y = f(x)
    h = (b - a) / n
    integral = (h / 3) * (y[0] + 4 * np.sum(y[1:-1:2]
                                            ) + 2 * np.sum(y[2:-2:2]) + y[-1])
    return integral


def forward_difference(f, x, h):
    return (f(x + h) - f(x)) / h


def central_difference(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)


def second_derivative(f, x, h):
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)


def eulers_method(f, y0, t0, t_end, h):
    n = int((t_end - t0) / h)
    t_values = np.linspace(t0, t_end, n+1)
    y_values = np.zeros(n+1)
    y_values[0] = y0
    for i in range(1, n+1):
        y_values[i] = y_values[i-1] + h * f(t_values[i-1], y_values[i-1])
    return t_values, y_values


def runge_kutta_4(f, y0, t0, t_end, h):
    n = int((t_end - t0) / h)
    t_values = np.linspace(t0, t_end, n+1)
    y_values = np.zeros(n+1)
    y_values[0] = y0
    for i in range(1, n+1):
        t = t_values[i-1]
        y = y_values[i-1]
        k1 = h * f(t, y)
        k2 = h * f(t + h/2, y + k1/2)
        k3 = h * f(t + h/2, y + k2/2)
        k4 = h * f(t + h, y + k3)
        y_values[i] = y + (k1 + 2*k2 + 2*k3 + k4) / 6
    return t_values, y_values


def heat_equation_fdm(alpha, u0, t_end, x_end, y_end, dx, dy, dt):
    nx, ny = int(x_end / dx) + 1, int(y_end / dy) + 1
    nt = int(t_end / dt)
    u = np.zeros((nt+1, nx, ny))
    u[0] = u0

    for n in range(0, nt):
        for i in range(1, nx-1):
            for j in range(1, ny-1):
                u[n+1, i, j] = (u[n, i, j] +
                                alpha * dt / dx**2 * (u[n, i+1, j] - 2*u[n, i, j] + u[n, i-1, j]) +
                                alpha * dt / dy**2 * (u[n, i, j+1] - 2*u[n, i, j] + u[n, i, j-1]))
    return u


def bisection_method(f, a, b, tol):
    if f(a) * f(b) >= 0:
        raise ValueError("Function must have different signs at a and b")

    while (b - a) / 2 > tol:
        c = (a + b) / 2
        if f(c) == 0:
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2


def newton_raphson(f, df, x0, tol, max_iter):
    x = x0
    for _ in range(max_iter):
        x_new = x - f(x) / df(x)
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    raise ValueError("Newton-Raphson method did not converge")


def main():
    # Example usage
    def sin(x): return np.sin(x)

    a, b, n = 0, np.pi, 1000
    tp_result = trapezoidal_rule(sin, a, b, n)
    print(f"Trapezoidal Rule Result: {tp_result}")

    sp_result = simpsons_rule(sin, a, b, 1000)
    print(f"Simpson's Rule Result: {sp_result}")

    def pow(x): return x**2

    x, h = 2.0, 1e-5
    fd_result = forward_difference(pow, x, h)
    cd_result = central_difference(pow, x, h)
    print(f"Forward Difference Result: {fd_result}")
    print(f"Central Difference Result: {cd_result}")

    second_deriv_result = second_derivative(pow, x, h)
    print(f"Second Derivative Result: {second_deriv_result}")

    def euler(_, y): return -2 * y + 1

    y0, t0, t_end, h = 0, 0, 10, 0.1
    _, y_values = eulers_method(euler, y0, t0, t_end, h)
    print(f"Euler's Method Result: {y_values[-1]}")

    _, y_values = runge_kutta_4(euler, y0, t0, t_end, h)
    print(f"Runge-Kutta Result: {y_values[-1]}")

    alpha, x_end, y_end, t_end = 0.01, 1.0, 1.0, 0.1
    dx, dy, dt = 0.1, 0.1, 0.01
    u0 = np.zeros((int(x_end / dx) + 1, int(y_end / dy) + 1))
    u = heat_equation_fdm(alpha, u0, t_end, x_end, y_end, dx, dy, dt)
    print(f"Heat Equation FDM Result at final time step: {u[-1]}")

    def f(x): return x**3 - x - 2
    a, b, tol = 1, 2, 1e-5
    root = bisection_method(f, a, b, tol)
    print(f"Bisection Method Result: {root}")

    def df(x): return 3*x**2 - 1
    root = newton_raphson(f, df, 1.5, 1e-5, 100)
    print(f"Newton-Raphson Method Result: {root}")


if __name__ == '__main__':
    main()
