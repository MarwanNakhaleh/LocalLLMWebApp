from time import time

from flask import request
from flask.blueprints import Blueprint
from flask_cors import cross_origin

from .helpers import json_response, api_response
from .data import context_data

context = Blueprint('context', __name__)
healthcheck = Blueprint('healthcheck', __name__)

@context.route(context_data.endpoint, methods=["POST"])
@cross_origin(headers=['Content-Type'])
def post_context():
    start = time()
    args = {}
    try:
        for key in context_data.args:
            args[key] = request.args.get(key)

        elapsed_time = time() - start
        results = json_response(
            args, 
            context_data.endpoint, 
            {
                "message": request.json['context']
            },
            elapsed_time
        )
        resp = api_response(results, context_data.endpoint)
    except Exception as e:
        results = {
            "error": str(e)
        }
        resp = api_response(results, context_data.endpoint, None, None, 400)
    return resp

@healthcheck.route('/', methods=["GET"])
def get():
    return api_response({
        "status": "UP"
    }, "/")