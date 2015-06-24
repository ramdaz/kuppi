import random, hashlib

def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
  
    return ''.join(random.choice(allowed_chars) for i in range(length))
