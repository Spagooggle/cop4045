# -*- coding: utf-8 -*-
def main() -> None:

    # Part a
    answer_a = [
        (a, b, c, d)
        for a in range(1, 11)
        for b in range(1, 11)
        for c in range(1, 11)
        for d in range(1, 11)
        if len({a, b, c, d}) == 4
        and a ** 2 + b ** 2 == c ** 2 + d ** 2
    ]

    print("Part a:")
    print(answer_a)
    print()

    # Part b
    words = ["One", "SEVEN", "three", "two", "Ten"]

    answer_b = [
        (word.lower(), len(word))
        for word in words
        if len(word) < 5
    ]

    print("Part b:")
    print(answer_b)
    print()

    # Part c
    names = [
        "Ryan Thomas Gosling",
        "Brian Robert Fornaro",
    ]

    answer_c = [
        f"{name.split()[0]} {name.split()[1][0]}. {name.split()[2]}"
        for name in names
    ]

    print("Part c:")
    print(answer_c)
    print()

    # part d
    lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
    lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]

    answer_d = [
        (word1, word2)
        for word1 in lst1
        for word2 in lst2
        if sorted(word1.lower()) == sorted(word2.lower())
    ]

    print("Part d:")
    print(answer_d)
    print()

    # Part e
    s = ["one", "two", "three"]

    answer_e = {word: len(word) for word in s}

    print("Part e:")
    print(answer_e)
    print()

    # Part f
    text = "Hello world"

    answer_f = {
        i: character
        for i, character in enumerate(text)
        if character.lower() in "aeiou"
    }

    print("Part f:")
    print(answer_f)


if __name__ == "__main__":
    main()