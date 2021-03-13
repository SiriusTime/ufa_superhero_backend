import hashlib
import random
import string


def crypt(main_string):
    return hashlib.sha256(main_string.encode()).hexdigest()


def generate_code(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
