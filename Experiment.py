import random
import os
import hashlib as hl

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
            key_char = key[i % key_length].lower()  
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

def calculate_hashes(content):
    binary_data = content.encode("utf-8")
    md5_hash = hl.md5(binary_data).hexdigest()
    sha1_hash = hl.sha1(binary_data).hexdigest()
    return md5_hash, sha1_hash

def encrypt_file(input_file_name):
    try:
        current_directory = os.getcwd()

        input_file_path = os.path.join(current_directory, input_file_name)
        output_file_name = f'E_{input_file_name}'
        output_file_path = os.path.join(current_directory, output_file_name)

        vigenere_key = input("Enter the Vigenere key: ")

        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            first_word_length = len(content.split()[0])
            caesar_shift_1 = first_word_length
            caesar_shift_2 = first_word_length
            caesar_encrypted_content = caesar_encrypt(content, -caesar_shift_1)
            vigenere_encrypted_content = vigenere_encrypt(caesar_encrypted_content, vigenere_key)
            final_encrypted_content = caesar_encrypt(vigenere_encrypted_content, -caesar_shift_2)
            reversed_content = reverse_text(final_encrypted_content)

            md5_original, sha1_original = calculate_hashes(content)

            public_key, private_key = generate_keypair()
            rsa_encrypted_content = encrypt_rsa(reversed_content, public_key)

            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(','.join(map(str, rsa_encrypted_content)))

            with open(f'{output_file_path[:-4]}_key.txt', 'w', encoding='utf-8') as key_file:
                key_file.write(','.join(map(str, private_key)))

            vigenere_key_file_path = f'{output_file_path[:-4]}_vigenere_key.txt'
            with open(vigenere_key_file_path, 'w', encoding='utf-8') as vigenere_key_file:
                vigenere_key_file.write(vigenere_key)

        print(f"Encryption successful. RSA encrypted content saved to {output_file_path}")
        print(f"Vigenere key saved to {vigenere_key_file_path}")
        print(f"Private key saved to {output_file_path[:-4]}_key.txt")

    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def decrypt_file(input_file_name):
    private_key = None
    md5_original, sha1_original = None, None  
    try:
        current_directory = os.getcwd()

        input_file_path = os.path.join(current_directory, input_file_name)
        base_name = os.path.basename(input_file_path)
        prefix, suffix = base_name.split('_', 1)

        if prefix in ['E', 'D']:
            file_name, extension = os.path.splitext(suffix)
            vigenere_key_file_path = os.path.join(current_directory, f'{file_name}_vigenere_key.txt')
            print(f"Attempted Vigenere key file path: {vigenere_key_file_path}")
            if not os.path.exists(vigenere_key_file_path):
                raise FileNotFoundError(f"The Vigenere key file '{vigenere_key_file_path}' does not exist.")

            with open(vigenere_key_file_path, 'r', encoding='utf-8') as vigenere_key_file:
                vigenere_key = vigenere_key_file.read()

            private_key_file_path = os.path.join(current_directory, f'{file_name}_key.txt')
            if not os.path.exists(private_key_file_path):
                raise FileNotFoundError(f"The private key file '{private_key_file_path}' does not exist.")

            with open(private_key_file_path, 'r', encoding='utf-8') as private_key_file:
                private_key_str = private_key_file.read()

            private_key = tuple(map(int, private_key_str.split(',')))

            with open(input_file_path, 'r', encoding='utf-8') as file:
                content = file.read().split(',')
                rsa_encrypted_content = [int(char) for char in content]

            original_content = decrypt_rsa(rsa_encrypted_content, private_key)
            original_content = reverse_text(original_content)
            md5_original, sha1_original = calculate_hashes(original_content)

            decrypted_content = decrypt_rsa(rsa_encrypted_content, private_key)
            decrypted_content = reverse_text(decrypted_content)

            first_word_length = len(decrypted_content.split()[0])
            caesar_shift_1 = first_word_length
            caesar_shift_2 = first_word_length

            vigenere_decrypted_content = caesar_decrypt(decrypted_content, -caesar_shift_2)
            vigenere_decrypted_content = vigenere_decrypt(vigenere_decrypted_content, vigenere_key)

            md5_decrypted, sha1_decrypted = calculate_hashes(decrypted_content)

            final_decrypted_content = caesar_decrypt(vigenere_decrypted_content, -caesar_shift_1)

            output_file_name = f'D_{suffix}'
            output_file_path = os.path.join(current_directory, output_file_name)

            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(final_decrypted_content)

            print(f"Decryption successful. Decrypted content saved to {output_file_path}")

            if md5_original == md5_decrypted and sha1_original == sha1_decrypted:
                print("Hash values match. Content is intact.")
            else:
                print("Hash values do not match. Content may be corrupted.")

            print(f"\nOriginal MD5: {md5_original}")
            print(f"Original SHA1: {sha1_original}")
            print(f"\nDecrypted MD5: {md5_decrypted}")
            print(f"Decrypted SHA1: {sha1_decrypted}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")





if __name__ == "__main__":
    action = input("Welcome!\n\n\nE - Encryption\nD - Decryption\nInput:").upper()

    if action == 'E':
        input_file_name = input("\nEnter the name of the text file to encrypt (filename).txt:  ")
        encrypt_file(input_file_name)

    elif action == 'D':
        input_file_name = input("\nEnter the name of the text file to decrypt (filename).txt: ")
        decrypt_file(input_file_name)

    else:
        print("Invalid option. Please enter 'E' for encryption or 'D' for decryption.")
 
