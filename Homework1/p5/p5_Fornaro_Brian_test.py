"""Tests for the Caesar cipher program."""

import unittest

import p5_Fornaro_Brian


class CaesarCipherTest(unittest.TestCase):
    """Tests the Caesar cipher functions."""

    def test_caesar_cipher_preserves_case_and_spaces(self):
        self.assertEqual(
            p5_Fornaro_Brian.caesar_cipher("Hello World", 3),
            "Khoor Zruog",
        )

    def test_caesar_cipher_wraps_around_alphabet(self):
        self.assertEqual(p5_Fornaro_Brian.caesar_cipher("XyZ", 4), "BcD")

    def test_caesar_cipher_preserves_nonletters(self):
        self.assertEqual(
            p5_Fornaro_Brian.caesar_cipher("Meet at 5:30!", 1),
            "Nffu bu 5:30!",
        )

    def test_caesar_cipher_accepts_negative_and_large_shifts(self):
        self.assertEqual(p5_Fornaro_Brian.caesar_cipher("Abc", -1), "Zab")
        self.assertEqual(p5_Fornaro_Brian.caesar_cipher("Abc", 27), "Bcd")

    def test_caesar_decipher_restores_original_text(self):
        encrypted = p5_Fornaro_Brian.caesar_cipher("College Python!", 7)
        self.assertEqual(
            p5_Fornaro_Brian.caesar_decipher(encrypted, 7),
            "College Python!",
        )

    def test_letter_frequency_ignores_case_and_nonletters(self):
        frequencies = p5_Fornaro_Brian.letter_frequency("A big apple! 123")

        self.assertEqual(frequencies["a"], 2)
        self.assertEqual(frequencies["p"], 2)
        self.assertEqual(frequencies["b"], 1)
        self.assertEqual(frequencies["z"], 0)
        self.assertEqual(len(frequencies), 26)

    def test_letter_frequency_with_empty_text(self):
        expected = {letter: 0 for letter in "abcdefghijklmnopqrstuvwxyz"}
        self.assertEqual(p5_Fornaro_Brian.letter_frequency(""), expected)


if __name__ == "__main__":
    unittest.main()
