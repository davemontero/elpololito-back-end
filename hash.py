from argon2 import PasswordHasher, exceptions

ph = PasswordHasher()

def hashPassword(password):
    hash = ph.hash(password)
    return hash

def verifyPassword(dbpass, password):
    try:
        ph.verify(dbpass, password)
        return True
    except exceptions.VerificationError as e: 
        return e

