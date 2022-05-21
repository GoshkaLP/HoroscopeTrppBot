from flask import Flask
from app.controllers.scheduler_controller import scheduler
from app.views.node import node
from app.controllers.redis_controller import update_forecasts


def create_app(app_config=None):
    """
    Метод для создания объекта приложения с применением всех настроек
    :param app_config: конфиг приложения
    :return: объект приложения
    """
    app = Flask(__name__, instance_relative_config=False)

    update_forecasts()

    app.config.from_object(app_config)
    scheduler.init_app(app)

    app.register_blueprint(node)

    return app
