from flask_restful import Api
from flask import Flask, Blueprint

from src.tasks.routes import DirectTasks, ParametrizeTasks

from config import AppConfig


def create_app(db_url: str) -> Flask:
    # create flask app instance
    app = Flask(__name__)
    # create API Blueprint
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    # add API handlers
    api.add_resource(
        DirectTasks,
        '/tasks',
        resource_class_kwargs={'db_url': db_url}
    )
    api.add_resource(
        ParametrizeTasks,
        '/tasks/<int:task_id>',
        resource_class_kwargs={'db_url': db_url}
    )
    app.register_blueprint(api_bp)
    return app


if __name__ == '__main__':
    config = AppConfig()
    # create app, provide Database URL which build from ENV
    app_ = create_app(config.get_connection_uri())
    # set up app
    app_.config.update(config.get_app_config())
    # run app
    app_.run(host='0.0.0.0')
