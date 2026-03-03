#!/usr/bin/env python3
"""Simple fixture script for QuickView tests."""


def greet(name):
    return f"Hello, {name}!"


def add(a, b):
    return a + b


if __name__ == "__main__":
    print(greet("QuickView"))
    print(f"2 + 3 = {add(2, 3)}")
    print("Fixture script complete.")
