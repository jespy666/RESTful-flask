from flask_restful import Api
from flask import Flask, Blueprint

from config import BASE_DIR
from src.tasks.routes import DirectTasks, ParametrizeTasks


def create_app(db_url: str) -> Flask:
    app = Flask(__name__)
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
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
    app_ = create_app(f'sqlite:///{BASE_DIR}/dev.db')
    app_.run(debug=True)
