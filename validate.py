import re

def email_check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%', '-', '*']
    result = {
        "val": True,
        "msg": ""
    }

    if len(passwd) < 6:
        result["msg"] = 'length should be at least 6'
        result["val"] = False

    if len(passwd) > 50:
        result["msg"] = 'length should be not be greater than 50'
        result["val"] = False

    if not any(char.isdigit() for char in passwd):
        result["msg"] = 'Password should have at least one numeral'
        result["val"] = False

    if not any(char.isupper() for char in passwd):
        result["msg"] = 'Password should have at least one uppercase letter'
        result["val"] = False

    if not any(char.islower() for char in passwd):
        result["msg"] = 'Password should have at least one lowercase letter'
        result["val"] = False

    if not any(char in SpecialSym for char in passwd):
        result["msg"] = 'Password should have at least one of the symbols $@#-*'
        result["val"] = False
    if result:
        return result