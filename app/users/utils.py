import hashlib


def hash_password(salt, password):
    salted = (salt + password).encode()
    return hashlib.sha512(salted).hexdigest()
