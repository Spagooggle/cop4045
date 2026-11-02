# -*- coding: utf-8 -*-
from numbers import Real
from collections.abc import Iterable


class NVector:
    """A vector of real numbers stored in a list."""

    def __init__(self, *values: Real | Iterable[Real]) -> None:
        """Create a vector from one sequence or multiple numbers."""
        if len(values) == 0:
            raise TypeError("At least one argument is required")

        if len(values) == 1:
            self.elements = list(values[0])
        else:
            self.elements = list(values)

        for value in self.elements:
            if not isinstance(value, Real):
                raise TypeError("Vector elements must be numbers")

    def __len__(self) -> int:
        """Return the number of elements."""
        return len(self.elements)

    def __getitem__(self, index: int) -> Real:
        """Return the element at index, including negative indexes."""
        return self.elements[index]

    def __setitem__(self, index: int, value: Real) -> None:
        """Set the element at index to a real number."""
        if not isinstance(value, Real):
            raise TypeError("Value must be a number")
        self.elements[index] = value

    def __str__(self) -> str:
        """Return the vector as a string."""
        return f"NVector({self.elements})"

    def __eq__(self, other: object) -> bool:
        """Check if two NVectors contain the same values."""
        return isinstance(other, NVector) and self.elements == other.elements

    def __ne__(self, other: object) -> bool:
        """Check if two NVectors are different."""
        return not self == other

    def __add__(self, other: "NVector | Real") -> "NVector":
        """Add a number or a same-length vector to this vector."""
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must be the same length")
            result = [a + b for a, b in zip(self.elements, other.elements)]
        elif isinstance(other, Real):
            result = [a + other for a in self.elements]
        else:
            raise TypeError("Can only add an NVector or number")
        return NVector(result)

    def __radd__(self, other: Real) -> "NVector":
        """Allow a number to be added before the vector."""
        return self + other

    def __mul__(self, other: "NVector | Real") -> Real:
        """Return the sum of products with a number or same-length vector."""
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must be the same length")
            return sum(a * b for a, b in zip(self.elements, other.elements))
        if isinstance(other, Real):
            return sum(a * other for a in self.elements)
        raise TypeError("Can only multiply by an NVector or number")

    def __rmul__(self, other: Real) -> Real:
        """Allow a number to be multiplied before the vector."""
        return self * other

    @classmethod
    def zeros(cls, n: int) -> "NVector":
        """Create a vector of n zeros; n must be a nonnegative integer."""
        if not isinstance(n, int):
            raise TypeError("Dimension must be an integer")
        if n < 0:
            raise ValueError("Dimension cannot be negative")
        return cls([0] * n)


def testif(condition: bool, success: str, failure: str) -> None:
    """Print a message based on whether the test passes."""
    if condition:
        print("PASS:", success)
    else:
        print("FAIL:", failure)


def main() -> None:
    """Test the NVector methods."""
    print("Z23672108")
    print("Problem 1 - NVector Tests\n")

    numbers = [3, 0, 1, -1]
    v = NVector(numbers)
    numbers[0] = 20

    testif(v[0] == 3, "List was copied", "List copy failed")
    testif(NVector((3, 0, 1, -1)) == v, "Tuple constructor works", "Tuple failed")
    testif(NVector(3, 0, 1, -1) == v, "Multiple arguments work", "Arguments failed")
    testif(len(v) == 4, "Length works", "Length failed")
    testif(v[1] == 0 and v[-2] == 1, "Indexing works", "Indexing failed")

    v[2] = 5
    v[-1] = 10
    testif(v[2] == 5 and v[3] == 10, "Setitem works", "Setitem failed")
    testif(str(v) == "NVector([3, 0, 5, 10])", "Str works", "Str failed")
    testif(v == NVector(3, 0, 5, 10), "Equality works", "Equality failed")
    testif(v != NVector(1, 2, 3, 4), "Inequality works", "Inequality failed")

    a = NVector(3, 0, 1, -1)
    b = NVector(1, 2, 3, 4)
    testif(a + b == NVector(4, 2, 4, 3), "Vector addition works", "Addition failed")
    testif(a + 10 == NVector(13, 10, 11, 9), "Number addition works", "Number addition failed")
    testif(10 + a == NVector(13, 10, 11, 9), "Reflected addition works", "Reflected addition failed")
    testif(a * b == 2, "Vector multiplication works", "Vector multiplication failed")
    testif(a * 10 == 30, "Number multiplication works", "Number multiplication failed")
    testif(10 * a == 30, "Reflected multiplication works", "Reflected multiplication failed")
    testif(NVector.zeros(4) == NVector(0, 0, 0, 0), "Zeros works", "Zeros failed")

    try:
        a[10] = 5
        testif(False, "", "IndexError test failed")
    except IndexError:
        testif(True, "IndexError works", "")

    try:
        a + NVector(1, 2)
        testif(False, "", "ValueError test failed")
    except ValueError:
        testif(True, "ValueError works", "")


if __name__ == "__main__":
    main()
