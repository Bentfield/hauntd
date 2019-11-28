from google.oauth2 import id_token
from google.auth.transport import requests

import json

def decode_jwt_token(token, app):
	try:
		token = token.split(',')[0]

		# Needs to be using AWS KMS at some point
		creds = None
		with open('credentials_dev.json', 'r') as creds_file:
			creds = json.load(creds_file)
			client_id = creds['web']['client_id']
		idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)
		return idinfo
	except Exception as e:
		return None
	except ValueError as v:
		return None
