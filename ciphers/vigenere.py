class Vigenere:
    @staticmethod
    def encrypt(plaintext, key):
        ciphertext = ""
        text_length = len(plaintext)
        key_length = len(key)

        for i in range(text_length):
            current_char = ord(plaintext[i])
            key_char = key[i % key_length]
            shift = (ord(key_char) + 1) % 1114112

            current_char = (current_char + shift) % 1114112
            ciphertext += chr(current_char)

        return ciphertext

    @staticmethod
    def decrypt(ciphertext, key):
        decrypted_text = ""
        text_length = len(ciphertext)
        key_length = len(key)

        for i in range(text_length):
            current_char = ord(ciphertext[i])
            key_char = key[i % key_length]
            shift = (ord(key_char) + 1) % 1114112

            shifted_code = (current_char - shift) % 1114112
            decrypted_text += chr(shifted_code)

        return decrypted_text