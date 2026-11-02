from pathlib import Path
from tempfile import TemporaryDirectory, NamedTemporaryFile
import os


def _save(filename: str, text: str) -> None:
    """Replace a file only after its UTF-8 content is fully written."""
    path = Path(filename)
    temp_name = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                                dir=path.absolute().parent, delete=False) as file:
            temp_name = file.name
            file.write(text)
        os.replace(temp_name, path)
    finally:
        if temp_name is not None and os.path.exists(temp_name):
            os.unlink(temp_name)


def ed_read(filename: str, from_: int = 0, to: int = -1) -> str:
    """Return [from_, to); -1 means EOF. Invalid bounds raise IndexError."""
    if not isinstance(from_, int) or not isinstance(to, int):
        raise TypeError("Positions must be integers")
    text = Path(filename).read_text(encoding="utf-8")
    if to == -1:
        to = len(text)
    if from_ < 0 or to < from_ or to > len(text):
        raise IndexError("Positions are outside the file or reversed")
    return text[from_:to]


def ed_find(filename: str, search_str: str) -> list[int]:
    """Return all matching start positions; search_str must be nonempty."""
    if not isinstance(search_str, str):
        raise TypeError("Search text must be a string")
    if search_str == "":
        raise ValueError("Search text cannot be empty")
    text = ed_read(filename)
    positions = []
    for i in range(len(text) - len(search_str) + 1):
        if text.startswith(search_str, i):
            positions.append(i)
    return positions


def ed_replace(filename: str, search_str: str, replace_with: str,
               occurrence: int = -1) -> int:
    """Replace all (-1) or one indexed nonoverlapping match; return count."""
    if not isinstance(search_str, str) or not isinstance(replace_with, str):
        raise TypeError("Search and replacement text must be strings")
    if search_str == "":
        raise ValueError("Search text cannot be empty")
    if not isinstance(occurrence, int):
        raise TypeError("Occurrence must be an integer")
    if occurrence < -1:
        raise ValueError("Occurrence must be -1 or greater")
    text = ed_read(filename)
    if occurrence == -1:
        count = text.count(search_str)
        new_text = text.replace(search_str, replace_with)
    else:
        start = 0
        for _ in range(occurrence + 1):
            position = text.find(search_str, start)
            if position == -1:
                return 0
            start = position + len(search_str)
        new_text = text[:position] + replace_with + text[start:]
        count = 1
    if count > 0:
        _save(filename, new_text)
    return count


def ed_append(filename: str, string: str) -> int:
    """Append string, creating a missing file; return characters added."""
    if not isinstance(string, str):
        raise TypeError("Appended text must be a string")
    path = Path(filename)
    text = ed_read(filename) if path.exists() else ""
    _save(filename, text + string)
    return len(string)


def testif(condition: bool, test_name: str) -> bool:
    """Print a test result and return whether it passed."""
    print(test_name + ": " + ("PASS" if condition else "FAIL"))
    return condition


def test_ed_find() -> bool:
    """Test repeated, missing, overlapping, and UTF-8 matches."""
    with TemporaryDirectory() as folder:
        filename = str(Path(folder) / "find.txt")
        _save(filename, "01234567890123456789")
        results = [testif(ed_find(filename, "345") == [3, 13], "find repeated")]
        results.append(testif(ed_find(filename, "356") == [], "find missing"))
        _save(filename, "aaaa")
        results.append(testif(ed_find(filename, "aa") == [0, 1, 2],
                              "find overlapping"))
        _save(filename, "café café")
        results.append(testif(ed_find(filename, "é") == [3, 8], "find UTF-8"))
    return all(results)


def test_ed_replace() -> bool:
    """Test all, indexed, missing, and out-of-range replacements."""
    with TemporaryDirectory() as folder:
        filename = str(Path(folder) / "replace.txt")
        original = "01234567890123456789"
        _save(filename, original)
        count = ed_replace(filename, "345", "ABCDE")
        results = [testif(count == 2 and ed_read(filename) ==
                          "012ABCDE6789012ABCDE6789", "replace all")]
        _save(filename, original)
        count = ed_replace(filename, "345", "ABCDE", 1)
        results.append(testif(count == 1 and ed_read(filename) ==
                              "0123456789012ABCDE6789", "replace indexed"))
        _save(filename, original)
        results.append(testif(ed_replace(filename, "xyz", "!") == 0 and
                              ed_read(filename) == original, "replace missing"))
        results.append(testif(ed_replace(filename, "345", "!", 2) == 0 and
                              ed_read(filename) == original, "replace out of range"))
    return all(results)


def main() -> None:
    """Run tests and demonstrate all four editor commands."""
    print("Brian Fornaro")
    print("Z23672108")
    find_ok = test_ed_find()
    replace_ok = test_ed_replace()
    if not (find_ok and replace_ok):
        raise AssertionError("Unit tests failed")
    print("All 8 tests passed.")
    with TemporaryDirectory() as folder:
        filename = str(Path(folder) / "example.txt")
        print("Append:", ed_append(filename, "0123456789"))
        print("Append:", ed_append(filename, "0123456789"))
        print("Read [3, 9):", ed_read(filename, 3, 9))
        print("Read from 3:", ed_read(filename, 3))
        print("Find 345:", ed_find(filename, "345"))
        print("Replaced:", ed_replace(filename, "345", "ABCDE", 1))
        print("Final text:", ed_read(filename))


if __name__ == "__main__":
    main()