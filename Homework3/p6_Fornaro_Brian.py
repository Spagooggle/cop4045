from __future__ import annotations

import unittest


class Entry:
    """A named storage entry with an optional parent."""

    def __init__(self, name: str, parent: Entry | None = None) -> None:
        """Store the entry name and parent; None identifies a root."""
        self.name = name
        self._parent = parent

    def parent(self) -> Entry | None:
        """Return this entry's parent, or None for a root."""
        return self._parent

    def size(self) -> int:
        """Return storage size as implemented by a subclass."""
        raise NotImplementedError("Subclasses must define size()")

    def absolute_path(self) -> list[Entry]:
        """Recursively return entries from this entry through the root."""
        if self._parent is None:
            return [self]
        return [self] + self._parent.absolute_path()


class File(Entry):
    """A file using a nonnegative integer number of bytes."""

    def __init__(self, name: str, bytes_used: int,
                 parent: Entry | None = None) -> None:
        """Create a file; reject negative or noninteger byte counts."""
        super().__init__(name, parent)
        self.bytes_used = bytes_used

    @property
    def bytes_used(self) -> int:
        """Return the file's byte count."""
        return self._bytes_used

    @bytes_used.setter
    def bytes_used(self, value: int) -> None:
        """Set a nonnegative integer byte count."""
        if not isinstance(value, int):
            raise TypeError("bytes_used must be an integer")
        if value < 0:
            raise ValueError("bytes_used cannot be negative")
        self._bytes_used = value

    def size(self) -> int:
        """Return the bytes used by this file."""
        return self.bytes_used


class Folder(Entry):
    """A folder containing files and other folders."""

    def __init__(self, name: str, parent: Entry | None = None) -> None:
        """Create an empty folder with an optional parent."""
        super().__init__(name, parent)
        self._children: list[Entry] = []

    def add(self, entry: Entry) -> None:
        """Add a child and set its parent; reject another folder's child."""
        if not isinstance(entry, Entry):
            raise TypeError("Child must be an Entry")
        if entry.parent() is not None and entry.parent() is not self:
            raise ValueError("Entry already has another parent")
        if entry not in self._children:
            self._children.append(entry)
            entry._parent = self

    def children(self) -> tuple[Entry, ...]:
        """Return the children as an immutable tuple."""
        return tuple(self._children)

    def size(self) -> int:
        """Return the total size through each child's common size method."""
        total = 0
        for child in self._children:
            total += child.size()
        return total


def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
    """Return a qualifying file or recursively search a folder's descendants."""
    if isinstance(entry, File):
        if entry.size() >= minimum_size:
            return [entry]
        return []
    if isinstance(entry, Folder):
        matches: list[File] = []
        for child in entry.children():
            matches.extend(find_large_files(child, minimum_size))
        return matches
    return []


def build_example() -> tuple[Folder, File]:
    """Build university/courses/cop4045/homework with files at several levels."""
    root = Folder("university")
    courses = Folder("courses")
    course = Folder("cop4045")
    homework = Folder("homework")
    root.add(File("readme.txt", 100))
    root.add(courses)
    courses.add(File("catalog.pdf", 1200))
    courses.add(course)
    course.add(File("notes.pdf", 600))
    course.add(homework)
    program = File("p6_Fornaro_Brian.py", 300)
    homework.add(program)
    homework.add(File("results.png", 2400))
    return root, program


class TestEntries(unittest.TestCase):
    """Test recursive searches, paths, and storage totals."""

    def setUp(self) -> None:
        """Create a fresh hierarchy before each test."""
        self.root, self.program = build_example()

    def test_find_two_thresholds(self) -> None:
        """Find nested files at two size thresholds."""
        self.assertEqual([f.name for f in find_large_files(self.root, 600)],
                         ["catalog.pdf", "notes.pdf", "results.png"])
        self.assertEqual([f.name for f in find_large_files(self.root, 1500)],
                         ["results.png"])

    def test_find_file(self) -> None:
        """Include a file at the threshold and exclude it above the threshold."""
        self.assertEqual(find_large_files(self.program, 300), [self.program])
        self.assertEqual(find_large_files(self.program, 301), [])

    def test_find_empty_folder(self) -> None:
        """An empty folder has no matching files."""
        self.assertEqual(find_large_files(Folder("empty"), 0), [])

    def test_find_no_matches(self) -> None:
        """Return an empty list when the threshold exceeds every file."""
        self.assertEqual(find_large_files(self.root, 10000), [])

    def test_find_zero_byte_file(self) -> None:
        """A zero-byte file qualifies at threshold zero."""
        empty = File("empty.txt", 0)
        self.assertEqual(find_large_files(empty, 0), [empty])

    def test_root_path(self) -> None:
        """The root path contains only the root object."""
        self.assertEqual(self.root.absolute_path(), [self.root])

    def test_nested_path(self) -> None:
        """Return actual entry objects in current-to-root order."""
        path = self.program.absolute_path()
        self.assertIs(path[0], self.program)
        self.assertIs(path[-1], self.root)
        self.assertEqual([entry.name for entry in path],
                         ["p6_Fornaro_Brian.py", "homework", "cop4045",
                          "courses", "university"])
        self.assertIs(path[1], self.program.parent())

    def test_folder_path(self) -> None:
        """A folder also supports the inherited recursive path method."""
        courses = self.root.children()[1]
        self.assertEqual(courses.absolute_path(), [courses, self.root])

    def test_size_and_children(self) -> None:
        """One outer size call handles files and nested folders."""
        self.assertEqual(self.root.size(), 4600)
        self.assertIsInstance(self.root.children(), tuple)
        self.assertEqual(Folder("empty").size(), 0)

    def test_negative_bytes(self) -> None:
        """Reject a negative file size."""
        with self.assertRaises(ValueError):
            File("invalid.txt", -1)


def main() -> None:
    """Show polymorphism, recursive searches, paths, and unit test results."""
    print("Brian Fornaro")
    print("FAU student ID: Z23672108")
    root, program = build_example()
    print("Total size:", root.size(), "bytes")
    for entry in root.children():
        print(entry.name, "uses", entry.size(), "bytes")
    print("Files at least 600 bytes:",
          [file.name for file in find_large_files(root, 600)])
    print("Files at least 1500 bytes:",
          [file.name for file in find_large_files(root, 1500)])
    print("Path from file to root:",
          " -> ".join(entry.name for entry in program.absolute_path()))
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestEntries)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)


if __name__ == "__main__":
    main()
