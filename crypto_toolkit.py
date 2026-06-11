import hashlib
import base64
import os

def hash_text(text):
    print("\n=== HASH GENERATOR ===")
    print(f"MD5:    {hashlib.md5(text.encode()).hexdigest()}")
    print(f"SHA1:   {hashlib.sha1(text.encode()).hexdigest()}")
    print(f"SHA256: {hashlib.sha256(text.encode()).hexdigest()}")
    print(f"SHA512: {hashlib.sha512(text.encode()).hexdigest()}")

def hash_file(filepath):
    print("\n=== FILE HASH (Evidence Integrity) ===")
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        print(f"MD5:    {hashlib.md5(data).hexdigest()}")
        print(f"SHA256: {hashlib.sha256(data).hexdigest()}")
        print("Use these hashes to verify file was not tampered!")
    except:
        print("File not found!")

def encode_base64(text):
    encoded = base64.b64encode(text.encode()).decode()
    print(f"\nBase64 Encoded: {encoded}")
    return encoded

def decode_base64(text):
    try:
        decoded = base64.b64decode(text).decode()
        print(f"\nBase64 Decoded: {decoded}")
    except:
        print("Invalid base64!")

def caesar_cipher(text, shift, mode):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            if mode == 'encrypt':
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char
    print(f"\nCaesar Result: {result}")

def verify_files(file1, file2):
    print("\n=== FILE INTEGRITY CHECK ===")
    try:
        with open(file1, 'rb') as f:
            h1 = hashlib.sha256(f.read()).hexdigest()
        with open(file2, 'rb') as f:
            h2 = hashlib.sha256(f.read()).hexdigest()
        if h1 == h2:
            print("✅ Files are IDENTICAL - not tampered!")
        else:
            print("🚨 Files are DIFFERENT - possible tampering!")
        print(f"File 1: {h1}")
        print(f"File 2: {h2}")
    except:
        print("File not found!")

while True:
    print("\n=============================")
    print("  CYBER CELL CRYPTO TOOLKIT")
    print("  By Jayesh Goyal")
    print("=============================")
    print("1. Hash Text")
    print("2. Hash File")
    print("3. Base64 Encode")
    print("4. Base64 Decode")
    print("5. Caesar Cipher Encrypt")
    print("6. Caesar Cipher Decrypt")
    print("7. Compare Two Files")
    print("8. Exit")
    choice = input("\nChoice: ")
    if choice == '1':
        t = input("Enter text: ")
        hash_text(t)
    elif choice == '2':
        f = input("Enter file path: ")
        hash_file(f)
    elif choice == '3':
        t = input("Enter text: ")
        encode_base64(t)
    elif choice == '4':
        t = input("Enter base64: ")
        decode_base64(t)
    elif choice == '5':
        t = input("Enter text: ")
        s = int(input("Shift (1-25): "))
        caesar_cipher(t, s, 'encrypt')
    elif choice == '6':
        t = input("Enter text: ")
        s = int(input("Shift (1-25): "))
        caesar_cipher(t, s, 'decrypt')
    elif choice == '7':
        f1 = input("File 1 path: ")
        f2 = input("File 2 path: ")
        verify_files(f1, f2)
    elif choice == '8':
        break
