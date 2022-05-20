from flask import Flask
from app.views.node import node


def create_app(app_config=None):
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(app_config)

    app.register_blueprint(node)

    return app
