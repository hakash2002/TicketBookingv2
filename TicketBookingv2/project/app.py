import os
from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager
app = None
from flask_caching import Cache
from celery_worker import make_celery
CORS(app,origins=["http://localhost:8080"])
cache = None
def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    CORS(app)
    db.init_app(app)
    cache = Cache(app)
    app.app_context().push()
    cache = Cache(app)
    return app,cache

app,cache = create_app()
celery = make_celery(app)

jwt = JWTManager(app)

from application.controllers import *

if __name__ == '__main__':
  # Run the Flask app
  db.create_all()
  app.run(host='0.0.0.0')