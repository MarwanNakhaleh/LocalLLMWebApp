import csv
import os

from flask import Flask
from flask_cors import CORS

from endpoints.endpoints import context, document_upload, healthcheck
from endpoints.data import context_data, upload_document_data
from database import db, StoredDocument

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    cors = CORS(app, resources={r"/*": {"origins": context_data.origins}})
    db.init_app(app)
    app.register_blueprint(context, url_prefix=context_data.api_prefix)
    app.register_blueprint(document_upload, url_prefix=upload_document_data.api_prefix)
    app.register_blueprint(healthcheck, url_prefix="")

    return app
        
def setup_database(app):
    with app.app_context():
        db.create_all()
    try:
        with open('stored_documents.csv', 'r', encoding="utf-8") as csvfile:
            next(csvfile)
            print("opened the csv file")
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                stored_document = StoredDocument()
                stored_document.id = int(row[0])
                stored_document.hash = row[1]
                stored_document.secure_filename = row[2]
                stored_document.sequence_number = row[3]
                db.session.add(stored_document)
            db.session.commit()
    except: 
        pass
        
if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    if not os.path.isfile('site.db'):
      setup_database(app)
    app.run(port=8000, host="0.0.0.0")