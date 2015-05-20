import random
from web.session import sha1

def password_salt():
    return "".join(chr(random.randint(33, 127)) for _ in xrange(64))


def password_hash(password, salt):
    return sha1(password + salt).hexdigest()


