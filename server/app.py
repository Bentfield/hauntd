from chalice import Chalice, Response, AuthResponse
from chalicelib import place, rating, auth
import pymysql.cursors
import base64
import boto3
import os
import logging

app = Chalice(app_name='hauntd')
app.log.setLevel(logging.DEBUG)
kms = boto3.client('kms')


def decrypt_kms(sec_key):
    kms = boto3.client('kms')
    response = kms.decrypt(CiphertextBlob=base64.b64decode(sec_key))  # decode key before decrypting it
    return response['Plaintext'].decode('utf-8')  # decrypted key comes in bytes literal form, must decode to utf-8


# Initialize database connection to MySQL
def get_SQL_conn():
    try:
        return pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=decrypt_kms(os.environ['DB_PASS']),
            db=os.environ['DB_NAME'],
            connect_timeout=10,
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        app.log.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        app.log.error(e)


# Application Routes
@app.route('/')
def index():
    return {'hello': 'world'}


@app.authorizer()
def jwt_auth(auth_request):
    token = auth_request.token
    decoded = auth.decode_jwt_token(token)
    app.log.debug(decoded)
    if decoded is not None:
        return AuthResponse(routes=['*'], principal_id=(decoded['email'], decoded['name']))
    else:
        return AuthResponse(routes=[], principal_id='')


def get_user_email(request):
    return request.context['authorizer']['principalId'][0]


def get_user_name(request):
    return request.context['authorizer']['principalId'][1]


@app.route('/place/{id}', methods=['GET'], cors=True)
def get_place(id: int) -> Response:
    return place.get_place(id, get_SQL_conn())


@app.route('/place/{id}', methods=['DELETE'], cors=True, authorizer=jwt_auth)
def delete_place(id: int) -> Response:
    email = get_user_email(app.current_request)
    return place.delete_place(id, email, get_SQL_conn())


@app.route('/place', methods=['POST'], cors=True, authorizer=jwt_auth)
def post_place() -> Response:
    request = app.current_request
    username = get_user_name(request)
    email = get_user_email(request)
    return place.post_place(request, username, email, get_SQL_conn())


@app.route('/place/{id}', methods=['PATCH'], cors=True, authorizer=jwt_auth)
def patch_place(id: int) -> Response:
    request = app.current_request
    email = get_user_email(request)
    return place.patch_place(id, request, email, get_SQL_conn())


@app.route('/rating/{id}', methods=['GET'], cors=True)
def get_place(id: int) -> Response:
    return rating.get_rating(id, get_conn())


@app.route('/rating', methods=['POST'], cors=True, authorizer=jwt_auth)
def post_rating() -> Response:
    request = app.current_request
    username = get_user_name(request)
    email = get_user_email(request)
    return rating.post_rating(request, email, username, get_conn())