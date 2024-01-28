from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
import os

CONFIG_NAME_MAPPER = {
    'local': 'config.LocalConfig',
    'prod': 'config.ProductionConfig',
    'dev': 'config.DevelopmentConfig',
    'test': 'config.TestingConfig'
}


class App:

    def __init__(self):
        if not hasattr(self, '_app'):
            self._app = Flask(__name__, static_folder='static')
            self._env = os.getenv('SPRING_PROFILES_ACTIVE')  # dev  test  prod
            self._app.config.from_object(CONFIG_NAME_MAPPER[self._env])
        if not hasattr(self, '_db'):
            self._db = SQLAlchemy(self._app)
        if not hasattr(self, '_redis_client'):
            self._redis_client = FlaskRedis(self._app, decode_responses=True)

    def __new__(cls, *args, **kwargs):
        if not hasattr(App, 'instance'):
            cls.instance = super(App, cls).__new__(cls)
        return cls.instance

    def register(self, path):
        self._app.register_blueprint(blueprint=path)

    def run(self):
        if self._env == 'local':
            self._app.run(host='127.0.0.1', debug=True, port=9999)
        else:
            self._app.run(host='0.0.0.0', debug=True, port=8080)

    @property
    def db(self):
        return self._db

    @property
    def redis_client(self):
        return self._redis_client

    @property
    def app(self):
        return self._app

    @property
    def env(self):
        return self._env
