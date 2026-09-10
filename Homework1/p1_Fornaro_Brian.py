# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt


while True:
    a_text = input("Enter a: ")

    if a_text == "":
        break

    a = float(a_text)
    b = float(input("Enter b: "))
    c = float(input("Enter c: "))

    d = b ** 2 - 4 * a * c

    if d < 0:
        print("no real solutions")

        middle = -b / (2 * a)
        start = middle - 5
        end = middle + 5

    elif d == 0:
        x1 = -b / (2 * a)
        print(f"one solution: {x1:.4f}")

        start = x1 - 5
        end = x1 + 5

    else:
        x1 = (-b - math.sqrt(d)) / (2 * a)
        x2 = (-b + math.sqrt(d)) / (2 * a)

        print(f"two solutions: x1={x1:.4f} x2={x2:.4f}")

        start = min(x1, x2) - 1
        end = max(x1, x2) + 1

    x_values = []
    y_values = []

    step = (end - start) / 49

    for i in range(50):
        x = start + i * step
        y = a * x ** 2 + b * x + c

        x_values.append(x)
        y_values.append(y)

    plt.plot(x_values, y_values)
    plt.axhline(0)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Quadratic Equation")
    plt.grid()
    plt.show()