from argon2 import PasswordHasher, exceptions
import random
import string

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

def get_random_password():
    sp_char = '$@#%-*'
    random_source = string.ascii_letters + string.digits + sp_char
    # select 1 lowercase
    password = random.choice(string.ascii_lowercase)
    # select 1 uppercase
    password += random.choice(string.ascii_uppercase)
    # select 1 digit
    password += random.choice(string.digits)
    # select 1 special symbol
    password += random.choice(sp_char)

    # generate other characters
    for i in range(6):
        password += random.choice(random_source)

    password_list = list(password)
    # shuffle all characters
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password