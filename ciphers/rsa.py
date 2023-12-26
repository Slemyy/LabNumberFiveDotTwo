import math
import random


class RSA:
    @staticmethod
    def __is_prime(number):
        if number <= 1:
            return False
        if number == 2:
            return True
        if number % 2 == 0:
            return False

        i = 3
        while i <= math.sqrt(number):
            if number % i == 0:
                return False
            i += 2
        return True

    def __generate_prime(self, lower_bound=50000, upper_bound=500000):
        num = 0
        while self.__is_prime(num) is False:
            num = random.randint(lower_bound, upper_bound)

        return num

    @staticmethod
    def __gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    def key_gen(self):
        p = self.__generate_prime()
        q = self.__generate_prime()
        n = p * q

        phi = (p - 1) * (q - 1)
        e = random.randint(1, phi)
        g = self.__gcd(e, phi)

        while g != 1:
            e = random.randint(1, phi)
            g = self.__gcd(e, phi)

        d = pow(e, -1, phi)
        return (e, n), (d, n)

    @staticmethod
    def encrypt(message, primary_key):
        key, n = primary_key
        return [pow(ord(char), key, n) for char in message]

    @staticmethod
    def decrypt(ciphertext, primary_key):
        key, n = primary_key
        return ''.join([chr(pow(char, key, n)) for char in ciphertext])
