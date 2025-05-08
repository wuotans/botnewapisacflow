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
CORS(app)


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

def api_wrap(route,route_id,func, methods=['GET'],*args,**kwargs):
    app.add_url_rule(route,route_id,lambda :func_standard_decorated(func,methods),methods=methods)

def api_wrap_for_send_files(route,route_id,func,*args,**kwargs):
    app.add_url_rule(route,route_id,lambda :func_standard_for_send_files_decorated(func),methods=['GET'])

def func_standard_decorated(func,method):
    logging.info(request.args)
    logging.info(request.data)
    if isinstance(request.data,bytes):
        decoded_str = request.data.decode()
        json_data = json.loads(decoded_str)
        return func(**json_data)
    return {'data':'Invalid parameters!'}


def func_standard_for_send_files_decorated(func):
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


def run(port):
    app.run(debug=False, host='0.0.0.0', port=port)


if __name__ == '__main__':
    pass
