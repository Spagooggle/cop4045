# -*- coding: utf-8 -*-
from typing import Any
import turtle


def _leaf(level: int, length: float, bend: float) -> None:
    """Draw a recursive leaf and restore the turtle's position and heading."""
    position = turtle.position()
    heading = turtle.heading()
    turtle.forward(length)
    junction = turtle.position()
    turtle.left(45)
    if level == 1:
        turtle.forward(length / 4)
    else:
        _leaf(level - 1, length * 0.4, bend)
    turtle.penup()
    turtle.goto(junction)
    turtle.setheading(heading - 45)
    turtle.pendown()
    if level == 1:
        turtle.forward(length / 4)
    else:
        _leaf(level - 1, length * 0.4, bend)
    turtle.penup()
    turtle.goto(junction)
    turtle.setheading(heading + bend)
    turtle.pendown()
    if level == 1:
        turtle.forward(length * 1.5)
    else:
        _leaf(level - 1, length * 0.65, bend)
    turtle.penup()
    turtle.goto(position)
    turtle.setheading(heading)
    turtle.pendown()


def _draw_leaf(level: int, length: float, bend: float) -> None:
    """Set up a vertical leaf; require a positive level and stem length."""
    if not isinstance(level, int):
        raise TypeError("Level must be an integer")
    if level < 1 or length <= 0:
        raise ValueError("Level and length must be positive")
    turtle.setup(900, 900)
    turtle.clear()
    turtle.title("Brian Fornaro - Recursive Leaf")
    turtle.speed(0)
    turtle.delay(0)
    turtle.tracer(0)
    turtle.penup()
    turtle.goto(0, -350)
    turtle.setheading(0)
    turtle.left(90)
    turtle.pendown()
    _leaf(level, length, bend)
    turtle.hideturtle()
    turtle.update()


def draw_leaf_straight(level: int, length: float) -> None:
    """Draw an upright recursive leaf with a straight central stem."""
    _draw_leaf(level, length, 0)


def draw_leaf_curved(level: int, length: float) -> None:
    """Draw an upright recursive leaf whose stem bends at each level."""
    _draw_leaf(level, length, 12)


def strB(n: int, base: int = 10) -> str:
    """Convert nonnegative integer n recursively to base 2 through 26."""
    if not isinstance(n, int) or not isinstance(base, int):
        raise TypeError("n and base must be integers")
    if n < 0 or not 2 <= base <= 26:
        raise ValueError("Require n >= 0 and 2 <= base <= 26")
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < base:
        return digits[n]
    return strB(n // base, base) + digits[n % base]


def Cnk_m(n: int, k: int,
          memo: dict[tuple[int, int], int] | None = None) -> int:
    """Return n choose k recursively with a dictionary; require 0 <= k <= n."""
    if not isinstance(n, int) or not isinstance(k, int):
        raise TypeError("n and k must be integers")
    if n < 0 or k < 0 or k > n:
        raise ValueError("Require 0 <= k <= n")
    if memo is None:
        memo = {}
    key = (n, k)
    if key not in memo:
        if k == 0 or k == n:
            memo[key] = 1
        else:
            memo[key] = Cnk_m(n - 1, k - 1, memo) + Cnk_m(n - 1, k, memo)
    return memo[key]


def run_Cnk(n: int, k: int) -> int:
    """Print and return a memoized binomial coefficient."""
    result = Cnk_m(n, k)
    print("Cnk_m(" + str(n) + ", " + str(k) + ") = " + str(result))
    return result


def make_pairs(seq1: list[Any], seq2: list[Any],
               accumulator: list[tuple[Any, Any]] | None = None
               ) -> list[tuple[Any, Any]]:
    """Recursively pair matching positions up to the shorter list's end."""
    if accumulator is None:
        accumulator = []
    if not seq1 or not seq2:
        return accumulator
    accumulator.append((seq1[0], seq2[0]))
    return make_pairs(seq1[1:], seq2[1:], accumulator)


def testif(condition: bool, test_name: str) -> bool:
    """Print the test result and return whether it passed."""
    print(test_name + ": " + ("PASS" if condition else "FAIL"))
    return condition


def test_make_pairs() -> bool:
    """Run five tests, including empty lists and unequal lengths."""
    test1 = testif(make_pairs([1, 2, 3], [4, 5, 6]) ==
                   [(1, 4), (2, 5), (3, 6)], "equal lengths")
    test2 = testif(make_pairs([1, 2, 3], [4, 5]) ==
                   [(1, 4), (2, 5)], "second list shorter")
    test3 = testif(make_pairs([1], [4, 5, 6]) ==
                   [(1, 4)], "first list shorter")
    test4 = testif(make_pairs([], [4, 5, 6]) == [], "first list empty")
    test5 = testif(make_pairs([1, 2, 3], []) == [], "second list empty")
    return test1 and test2 and test3 and test4 and test5


def test_strB() -> bool:
    """Run four tests for zero, binary, hexadecimal, and base 26."""
    test1 = testif(strB(0, 2) == "0", "strB zero")
    test2 = testif(strB(42, 2) == "101010", "strB binary")
    test3 = testif(strB(255, 16) == "FF", "strB hexadecimal")
    test4 = testif(strB(675, 26) == "PP", "strB base 26")
    return test1 and test2 and test3 and test4


def test_Cnk_m() -> bool:
    """Run four tests for base cases and nontrivial coefficients."""
    test1 = testif(Cnk_m(0, 0) == 1, "Cnk zero")
    test2 = testif(Cnk_m(7, 7) == 1, "Cnk k equals n")
    test3 = testif(Cnk_m(10, 3) == 120, "Cnk 10 choose 3")
    test4 = testif(Cnk_m(20, 10) == 184756, "Cnk 20 choose 10")
    return test1 and test2 and test3 and test4


def main() -> None:
    """Display student information and run the tests."""
    print("Brian Fornaro")
    print("Z23672108")
    base_ok = test_strB()
    binomial_ok = test_Cnk_m()
    pairs_ok = test_make_pairs()
    if not (base_ok and binomial_ok and pairs_ok):
        raise AssertionError("A test failed")
    print("All 13 tests passed.")
    print("strB(73, 8) =", strB(73, 8))
    print("strB(511, 16) =", strB(511, 16))
    run_Cnk(30, 15)
    run_Cnk(50, 6)


if __name__ == "__main__":
    main()
