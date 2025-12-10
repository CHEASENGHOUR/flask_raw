from flask import Flask
from config import Config
from api import api
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(api)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)