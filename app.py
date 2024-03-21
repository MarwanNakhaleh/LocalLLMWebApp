from flask import Flask
from flask_cors import CORS

from endpoints.endpoints import context, healthcheck
from endpoints.data import context_data

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = CORS(app, resources={r"/*": {"origins": context_data.origins}})
    app.register_blueprint(context, url_prefix=context_data.api_prefix)
    app.register_blueprint(healthcheck, url_prefix="")

    return app
        
if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    app.run(port=8000, host="0.0.0.0")