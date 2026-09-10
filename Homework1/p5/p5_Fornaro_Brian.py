"""Provides an interactive Caesar cipher program."""


def caesar_cipher(text, shift):
    """Encrypts text by shifting each letter by the given amount.

    Args:
        text: The string to encrypt.
        shift: The integer number of positions to shift each letter.

    Returns:
        The encrypted string with spaces and letter casing preserved.
    """
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    encrypted_text = ""

    for index in range(len(text)):
        character = text[index]

        if character in lowercase:
            old_position = lowercase.index(character)
            new_position = (old_position + shift) % len(lowercase)
            encrypted_text += lowercase[new_position]
        elif character in uppercase:
            old_position = uppercase.index(character)
            new_position = (old_position + shift) % len(uppercase)
            encrypted_text += uppercase[new_position]
        else:
            encrypted_text += character

    return encrypted_text


def caesar_decipher(cyphertext, shift):
    """Decrypts text that was encrypted with a Caesar cipher.

    Args:
        cyphertext: The Caesar-encrypted string to decrypt.
        shift: The integer shift used to encrypt the string.

    Returns:
        The original clear text.
    """
    return caesar_cipher(cyphertext, -shift)


def letter_frequency(text):
    """Counts alphabetic characters in text without regard to case.

    Args:
        text: The string whose letters will be counted.

    Returns:
        A dictionary containing a count for every lowercase letter.
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    frequencies = {}

    for letter in alphabet:
        frequencies[letter] = 0

    for index in range(len(text)):
        character = text[index].lower()
        if character in alphabet:
            frequencies[character] += 1

    return frequencies


def main():
    """Runs the interactive Caesar cipher menu."""
    message = ""
    shift = 0
    ciphered_text = ""

    while True:
        print("\nCaesar Cipher Menu")
        print("1. Enter a message")
        print("2. Specify a shift value")
        print("3. View the ciphered text")
        print("4. View the letter frequency breakdown")
        print("5. View the deciphered text")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == "1":
            message = input("Enter a message: ")
            ciphered_text = caesar_cipher(message, shift)
            print("Message saved.")
        elif choice == "2":
            try:
                shift = int(input("Enter an integer shift value: "))
                ciphered_text = caesar_cipher(message, shift)
                print("Shift value saved.")
            except ValueError:
                print("The shift value must be an integer.")
        elif choice == "3":
            ciphered_text = caesar_cipher(message, shift)
            print(f"Ciphered text: {ciphered_text}")
        elif choice == "4":
            frequencies = letter_frequency(message)
            print("Letter frequency for the original message:")
            for letter, count in frequencies.items():
                print(f"{letter}: {count}")
        elif choice == "5":
            ciphered_text = caesar_cipher(message, shift)
            clear_text = caesar_decipher(ciphered_text, shift)
            print(f"Deciphered text: {clear_text}")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Please choose a number from 1 through 6.")


if __name__ == "__main__":
    main()
