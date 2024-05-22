from flask import Flask
from src.tasks.routes import tasks_bp


def main():
    app = Flask(__name__)
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.run(debug=True)


if __name__ == '__main__':
    main()
