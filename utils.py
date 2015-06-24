import random, hashlib
from settings import *
from hashlib import *
def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
  
    return ''.join(random.choice(allowed_chars) for i in range(length))


def create_user(username, password, email):
    try:
	user = User.get(username=username)
	return False
    except:
	password = sha256(SECRET_KEY+password).hexdigest()
	user = User.create(username=username, password=password, email=email)
	return user
    return True
    
