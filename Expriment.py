import random
import os

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
            key_char = key[i % key_length].lower()  # Use lowercase for simplicity
            key_shift = ord(key_char) - ord('a')
            decrypted_char = chr((ord(char) - start - key_shift) % 26 + start)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

def reverse_text(text):
    return text[::-1]

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime():
    prime_candidate = random.randint(2**8, 2**16)
    while not is_prime(prime_candidate):
        prime_candidate += 1
    return prime_candidate

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    
    d = mod_inverse(e, phi)
    
    return ((n, e), (n, d))

def encrypt_rsa(message, public_key):
    n, e = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

def decrypt_rsa(encrypted_message, private_key):
    n, d = private_key
    decrypted_message = [chr(pow(char, d, n)) for char in encrypted_message]
    return ''.join(decrypted_message)

def encrypt_file(input_file_path, output_file_path, vigenere_key):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            first_word_length = len(content.split()[0])
            caesar_shift_1 = first_word_length
            caesar_shift_2 = first_word_length  # Use the same shift as the previous Caesar Cipher
            caesar_encrypted_content = caesar_encrypt(content, -caesar_shift_1)  # Corrected shift direction
            vigenere_encrypted_content = vigenere_encrypt(caesar_encrypted_content, vigenere_key)
            final_encrypted_content = caesar_encrypt(vigenere_encrypted_content, -caesar_shift_2)  # Corrected shift direction
            reversed_content = reverse_text(final_encrypted_content)

            # RSA Encryption
            public_key, private_key = generate_keypair()
            rsa_encrypted_content = encrypt_rsa(reversed_content, public_key)

            # Save RSA encrypted content to file
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(','.join(map(str, rsa_encrypted_content)))

            # Save private key to file without label
            with open(f'{output_file_path[:-4]}_keys.txt', 'w', encoding='utf-8') as key_file:
                key_file.write(','.join(map(str, private_key)))

            # Save Vigenere key to a separate file without label
            vigenere_key_file_path = f'{output_file_path[:-4]}_vigenere_key.txt'
            with open(vigenere_key_file_path, 'w', encoding='utf-8') as vigenere_key_file:
                vigenere_key_file.write(vigenere_key)

        print(f"Encryption successful. RSA encrypted content saved to {output_file_path}")
        print(f"Vigenere key saved to {vigenere_key_file_path}")
        print(f"Private key saved to {output_file_path[:-4]}_keys.txt")

    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def decrypt_file(input_file_path, output_file_path):
    private_key = None  # Initialize private_key variable
    try:
        # Check if the input file exists
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"The file '{input_file_path}' does not exist.")

        # Extract information from the input file name
        base_name = os.path.basename(input_file_path)
        prefix, file_name = base_name.split('_', 1)

        if prefix == 'Encrypted':
            # Extract the Vigenere key from the separate file without label
            vigenere_key_file_path = f'{input_file_path[:-4]}_vigenere_key.txt'
            if not os.path.exists(vigenere_key_file_path):
                raise FileNotFoundError(f"The Vigenere key file '{vigenere_key_file_path}' does not exist.")

            with open(vigenere_key_file_path, 'r', encoding='utf-8') as vigenere_key_file:
                vigenere_key = vigenere_key_file.read()

            # Extract the private key from the separate file without label
            private_key_file_path = f'{input_file_path[:-4]}_keys.txt'
            if not os.path.exists(private_key_file_path):
                raise FileNotFoundError(f"The private key file '{private_key_file_path}' does not exist.")

            with open(private_key_file_path, 'r', encoding='utf-8') as private_key_file:
                private_key_str = private_key_file.read()

            private_key = tuple(map(int, private_key_str.split(',')))

            # Decryption process
            with open(input_file_path, 'r', encoding='utf-8') as file:
                content = file.read().split(',')
                rsa_encrypted_content = [int(char) for char in content]

            decrypted_content = decrypt_rsa(rsa_encrypted_content, private_key)
            decrypted_content = reverse_text(decrypted_content)

            first_word_length = len(decrypted_content.split()[0])
            caesar_shift_1 = first_word_length
            caesar_shift_2 = first_word_length  # Use the same shift as the previous Caesar Cipher

            vigenere_decrypted_content = caesar_decrypt(decrypted_content, -caesar_shift_2)
            vigenere_decrypted_content = vigenere_decrypt(vigenere_decrypted_content, vigenere_key)

            # Extra Caesar decryption
            final_decrypted_content = caesar_decrypt(vigenere_decrypted_content, -caesar_shift_1)

            # Save decrypted content to file
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(final_decrypted_content)

            print(f"Decryption successful. Decrypted content saved to {output_file_path}")

        else:
            print("Invalid file format. Please provide an 'Encrypted' file for decryption.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")



# Example usage:
# Get user input for encryption or decryption
action = input("Do you want to (E)ncrypt or (D)ecrypt? ").upper()

if action == 'E':
    # Encryption process
    # Get input file name from the user
    input_file_name = input("Enter the name of the text file to encrypt (including extension): ")
    input_file_path = f'C:\\Users\\Zen\\Desktop\\Cryptography\\Cryptography\\{input_file_name}'

    # Generate output file name based on the input file name
    output_file_name = f'Encrypted_{input_file_name}'
    output_file_path = f'C:\\Users\\Zen\\Desktop\\Cryptography\\Cryptography\\{output_file_name}'

    # Get Vigenere key from the user
    vigenere_key = input("Enter the Vigenere key: ")

    encrypt_file(input_file_path, output_file_path, vigenere_key)

elif action == 'D':
    # Decryption process
    # Get input file name from the user
    input_file_name = input("Enter the name of the text file to decrypt (including extension): ")
    input_file_path = f'C:\\Users\\Zen\\Desktop\\Cryptography\\Cryptography\\{input_file_name}'

    # Generate output file name based on the input file name
    output_file_name = f'Decrypted_{input_file_name}'
    output_file_path = f'C:\\Users\\Zen\\Desktop\\Cryptography\\Cryptography\\{output_file_name}'

    decrypt_file(input_file_path, output_file_path)

else:
    print("Invalid option. Please enter 'E' for encryption or 'D' for decryption.")

