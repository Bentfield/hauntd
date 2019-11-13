from chalice import Chalice, Response
from chalicelib import place
import pymysql.cursors
import base64
import boto3
import os

app = Chalice(app_name='hauntd')
kms = boto3.client('kms')


def decrypt_kms(sec_key):
    kms = boto3.client('kms')
    response = kms.decrypt(CiphertextBlob=base64.b64decode(sec_key))  # decode key before decrypting it
    return response['Plaintext'].decode('utf-8')  # decrypted key comes in bytes literal form, must decode to utf-8


# Initialize database connection to MySQL
def get_conn():
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


@app.route('/place/{id}', methods=['GET'], cors=True)
def get_place(id: int) -> Response:
    return place.get_place(id, get_conn())


@app.route('/place/{id}', methods=['DELETE'], cors=True)
def delete_place(id: int) -> Response:
    return place.delete_place(id, get_conn())


@app.route('/place', methods=['POST'], cors=True)
def post_place() -> Response:
    request = app.current_request
    return place.post_place(request, get_conn())


@app.route('/place/{id}', methods=['PATCH'], cors=True)
def patch_place(id: int) -> Response:
    request = app.current_request
    return place.patch_place(id, request, get_conn())