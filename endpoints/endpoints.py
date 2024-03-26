from time import time

from flask import request
from flask.blueprints import Blueprint
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

from .helpers import json_response, api_response
from .data import context_data

context = Blueprint('context', __name__)
document_upload = Blueprint('document_upload', __name__)
healthcheck = Blueprint('healthcheck', __name__)

@context.route(context_data.endpoint, methods=["POST"])
@cross_origin(headers=['Content-Type'])
def post_context():
    start = time()
    args = {}
    try:
        for key in context_data.args:
            args[key] = request.args.get(key)

        shortname = request.json['shortname']
        if not shortname.isalpha():
            results = {
                "error": "context shortname must be letters only"
            }
            return api_response(results, context_data.endpoint, None, None, 400)

        elapsed_time = time() - start
        results = json_response(
            args, 
            context_data.endpoint, 
            {
                "context": request.json['context'],
                "shortname": shortname.lower()
            },
            elapsed_time
        )
        resp = api_response(results, context_data.endpoint)
    except Exception as e:
        results = {
            "error": str(e)
        }
        return api_response(results, context_data.endpoint, None, None, 400)
    return resp

@document_upload.route('/upload_document', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def upload_pdf():
    if 'file' not in request.files:
        return api_response({"error": "No file part"}, '/upload_document', None, None, 400)
    
    file = request.files['file']
    if file.filename == '':
        return api_response({"error": "No selected file"}, '/upload_document', None, None, 400)
    
    if file and file.content_type == 'application/pdf':
        filename = secure_filename(file.filename)
        
        try:
            process_pdf_file(file)  
            
            return api_response({"message": "PDF processed successfully", "filename": filename}, '/upload_pdf')
        except Exception as e:
            return api_response({"error": str(e)}, '/upload_pdf', None, None, 500)
    else:
        return api_response({"error": "Unsupported file type. Only PDF files are accepted."}, '/upload_pdf', None, None, 400)

@healthcheck.route('/', methods=["GET"])
def get():
    return api_response({
        "status": "UP"
    }, "/")
