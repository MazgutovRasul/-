import string


async def check_password(password):
    numbers = '1234567890'
    simb = string.punctuation
    a = True
    if len(password) > 8:
        if password.lower() != password:
            n, s = False, False
            for let in password:
                if let in numbers:
                    n = True
                if let in simb:
                    s = True
            if n and s:
                a = False
                return True
    if not a:
        return False
