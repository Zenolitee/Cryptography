def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            encrypted_char = chr((ord(char) - start + shift) % 26 + start)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def vigenere_encrypt(text, key):
    encrypted_text = ""
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            key_char = key[i % key_length].lower()  # Use lowercase for simplicity
            key_shift = ord(key_char) - ord('a')
            encrypted_char = chr((ord(char) - start + key_shift) % 26 + start)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

def vigenere_decrypt(text, key):
    decrypted_text = ""
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            key_char = key[i % key_length].lower()
            key_shift = ord(key_char) - ord('a')
            decrypted_char = chr((ord(char) - start - key_shift) % 26 + start)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text


def reverse_text(text):
    return text[::-1]

def encrypt_file(input_file_path, output_file_path, vigenere_key):
    try:
        with open(input_file_path, 'r') as file:
            content = file.read()
            first_word_length = len(content.split()[0])
            caesar_shift_1 = first_word_length
            caesar_shift_2 = first_word_length  # Use the same shift as the previous Caesar Cipher
            caesar_encrypted_content = caesar_encrypt(content, caesar_shift_1)
            vigenere_encrypted_content = vigenere_encrypt(caesar_encrypted_content, vigenere_key)
            final_encrypted_content = caesar_encrypt(vigenere_encrypted_content, caesar_shift_2)
            reversed_content = reverse_text(final_encrypted_content)
            
        with open(output_file_path, 'w') as file:
            file.write(reversed_content)
        
        print(f"Encryption successful. Encrypted content saved to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def decrypt_file(input_file_path, output_file_path, vigenere_key):
    try:
        with open(input_file_path, 'r') as file:
            content = file.read()
            first_word_length = len(content.split()[0])
            caesar_shift_1 = first_word_length
            caesar_shift_2 = first_word_length  # Use the same shift as the previous Caesar Cipher
            reversed_content = reverse_text(content)
            vigenere_decrypted_content = caesar_decrypt(reversed_content, caesar_shift_2)
            caesar_decrypted_content = vigenere_decrypt(vigenere_decrypted_content, vigenere_key)
            final_decrypted_content = caesar_decrypt(caesar_decrypted_content, caesar_shift_1)
            
        with open(output_file_path, 'w') as file:
            file.write(final_decrypted_content)
        
        print(f"Decryption successful. Decrypted content saved to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Get user input for encryption or decryption
action = input("Do you want to (E)ncrypt or (D)ecrypt? ").upper()

if action == 'E':
    # Encryption process
    # Get input file name from user
    input_file_name = input("Enter the name of the text file to encrypt (including extension): ")
    input_file_path = f'C:\\Users\\Zen\\Desktop\\Cryptography\\Cryptography\\{input_file_name}'

    # Generate output file name based on input file name
    output_file_name = f'Encrypted_{input_file_name}'
    output_file_path = f'C:\\Users\\Zen\\Desktop\\Cryptography\\Cryptography\\{output_file_name}'

    # Get Vigenere key from user
    vigenere_key = input("Enter the Vigenere key: ")

    encrypt_file(input_file_path, output_file_path, vigenere_key)

elif action == 'D':
    # Decryption process
    # Get input file name from user
    input_file_name = input("Enter the name of the text file to decrypt (including extension): ")
    input_file_path = f'C:\\Users\\Zen\\Desktop\\Cryptography\\Cryptography\\{input_file_name}'

    # Generate output file name based on input file name
    output_file_name = f'Decrypted_{input_file_name}'
    output_file_path = f'C:\\Users\\Zen\\Desktop\\Cryptography\\Cryptography\\{output_file_name}'

    # Get Vigenere key from user
    vigenere_key = input("Enter the Vigenere key: ")

    decrypt_file(input_file_path, output_file_path, vigenere_key)

else:
    print("Invalid option. Please enter 'E' for encryption or 'D' for decryption.")
