from hashlib import sha512
from config import SECRET_KEY
import jwt
import time

def pluralize(ingredient, quantity, plural='s'):
	words = ingredient.split(' ')
	if quantity > 1:
		words[0] = words[0] + plural
	return ' '.join(words)

def hash(password):
	hash = sha512()
	hash.update(password.encode('utf-8') + SECRET_KEY)
	passhash = hash.hexdigest()
	return passhash

def generate_jwt(username):
	accessToken = jwt.encode({
		"username": username,
		"exp": time.time() + 60*60*24
	}, SECRET_KEY, algorithm="HS256")
	return accessToken