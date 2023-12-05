def caesar_cipher(text, shift):
    result = ""

    for char in text:
        if char.isalpha():
            # Determine whether the character is uppercase or lowercase
            if char.isupper():
                result += chr((ord(char) + shift - ord('A')) % 26 + ord('A'))
            else:
                result += chr((ord(char) + shift - ord('a')) % 26 + ord('a'))
        else:
            # If the character is not an alphabet letter, keep it unchanged
            result += char

    return result

def main():
    # Get input from the user
    plaintext = input("Enter the text to encrypt: ")

    # Count the number of letters or words to determine the shift value
    is_sentence = '.' in plaintext
    if is_sentence:
        words = plaintext.split()
        shift = len(words[-1])
    else:
        letters = sum(char.isalpha() for char in plaintext)
        shift = letters

    # Encrypt the text using Caesar cipher
    ciphertext = caesar_cipher(plaintext, shift)

    # Display the encrypted text
    print("Encrypted text:", ciphertext)

if __name__ == "__main__":
    main()
