import re
import time
import logging
import ssl
from flask import Flask, request, send_from_directory, abort
from flask_restful import Api, Resource
from flask_limiter import Limiter
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from functools import wraps, partial
import threading as td
import secrets
import json

app = Flask(__name__)
api = Api(app)
limiter = Limiter(app=app, key_func=lambda: request.remote_addr, default_limits=["20 per minute", "3 per second"])
CORS(app)

global another_acess_key
another_acess_key=None

def generate_bearer_token():
    # Generate a secure random token using secrets
    token = secrets.token_urlsafe(32)  # You can change the length as needed
    return token


if not os.path.exists('parameters/api.txt'):
    os.makedirs('parameters',exist_ok=True)
    with open('parameters/api.txt','w') as f:
        API_KEY = f"Bearer {str(generate_bearer_token())}"
        f.write(API_KEY)
else:
    with open('parameters/api.txt','r') as f:
        API_KEY = f.read()



class InvalidFilePath(Exception):
    pass


class BadRequest(Exception):
    pass


class NotFound(Exception):
    pass


def secure_file_path(base_path, user_input):
    absolute_path = os.path.abspath(os.path.join(base_path, user_input))
    if not absolute_path.startswith(base_path):
        raise BadRequest("Invalid file path")
    if not os.path.exists(absolute_path):
        raise NotFound("File not found")
    return absolute_path

def set_another_header_acess_key(dict_acess_key):
    global another_acess_key
    another_acess_key = dict_acess_key
    logging.info(another_acess_key.keys())

def verify_another_header_keys_integrity(request_obj):
    global another_acess_key
    for key in another_acess_key:
        if request_obj.headers.get(key) == another_acess_key[key] or request_obj.args.get('token') == another_acess_key[key]:
            return True
    return False

def require_api_key(view_function):
    global another_acess_key
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        logging.info(request.args.get('token'))
        logging.info(API_KEY.replace('Bearer ',''))
        if request.args.get('token')==API_KEY.replace('Bearer ','') \
                or request.headers.get('Authorization') == API_KEY\
                or verify_another_header_keys_integrity(request):
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function


def api_wrap(route,route_id,func, methods=['GET'],*args,**kwargs):
    app.add_url_rule(route,route_id,lambda :func_standard_decorated(func,methods),methods=methods)

def api_wrap_for_send_files(route,route_id,func,*args,**kwargs):
    app.add_url_rule(route,route_id,lambda :func_standard_for_send_files_decorated(func),methods=['GET'])

@require_api_key
def func_standard_decorated(func,method):
    limiter.limit("20 per minute;3 per second")
    logging.info(request.args)
    logging.info(request.data)
    #if 'POST' in method:
    if isinstance(request.data,bytes):
        decoded_str = request.data.decode()
        json_data = json.loads(decoded_str)
        return func(**json_data)
    return {'data':'Invalid parameters!'}
    # if 'GET' in method:
    #     if request.args:
    #         return func(request.args)
    #     return {'data': 'Invalid parameters!'}

@require_api_key
def func_standard_for_send_files_decorated(func):
    limiter.limit("10 per minute;1 per second")
    logging.info(request.args)
    logging.info(request.data)
    if request.args:
        ret = func(request.args)
        if isinstance(ret,str):
            file_path = os.path.abspath(ret)
            barra = '\ '.strip()
            filename = file_path.split(barra)[-1]
            return send_from_directory(os.path.dirname(file_path), secure_filename(filename), as_attachment=True), 200
        else:
            return ret
    return {'data': 'Invalid parameters!'}


def run(port,sslmode:False):
    ssl_context=None
    if sslmode:
        #pip install flask-talisman
        from flask_talisman import Talisman
        talisman = Talisman(app)
        talisman.force_https = True
        path_cert = 'cert1.pem'
        path_private = 'privkey1.pem'
        logging.info(path_cert, path_private)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(path_cert, path_private)
        ssl_context = context
    app.run(debug=False, host='0.0.0.0', port=port,ssl_context=ssl_context)


if __name__ == '__main__':
    pass
