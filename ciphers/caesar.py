class Caesar:
    @staticmethod
    def encrypt(text, shift):
        result = ""
        for char in text:
            shifted_code = (ord(char) + shift) % 1114112  # Используем всю ASCII таблицу.

            result += chr(shifted_code)

        return result

    @staticmethod
    def decrypt(text, shift):
        return Caesar.encrypt(text, -shift)
