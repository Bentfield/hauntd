from google.oauth2 import id_token
from google.auth.transport import requests

import json


CLIENT_ID = "406470965278-g9duphf6roh47jvu380q5orrojbs8jld.apps.googleusercontent.com"


def decode_jwt_token(token):
	try:
		token = token.split(',')[0]
		idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
		return idinfo
	except Exception as e:
		return None
	except ValueError as v:
		return None
