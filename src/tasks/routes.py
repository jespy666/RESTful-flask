from typing import Tuple, Sequence

from flask import Blueprint, request, jsonify, Response

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from src.tasks.models import Task
from src.session import SessionFactory

from config import app_config


class TasksBlueprint(SessionFactory):

    def __init__(self) -> None:
        db_url: str = app_config.get_connection_uri()
        super().__init__(db_url)
        self.tasks_bp = Blueprint('tasks', __name__)
        self.set_urls()

    def create_task(self) -> Tuple[Response, int]:
        if request.method == 'POST':
            data: dict = request.json
            task = Task(
                title=data.get('title'),
                description=data.get('description')
            )
            session: Session = super().get_session()
            session.add(task)
            session.commit()
            session.close()
            return jsonify(task.to_dict()), 201

    def get_tasks(self) -> Tuple[Response, int]:
        if request.method == 'GET':
            session: Session = super().get_session()
            stmt = select(Task)
            tasks: Sequence[Task] = session.scalars(stmt).all()
            session.close()
            return jsonify([task.to_dict() for task in tasks]), 200

    def get_task(self, id: int) -> Tuple[Response, int]:
        if request.method == 'GET':
            session: Session = super().get_session()
            stmt = select(Task).where(Task.id == id)
            task: Task | None = session.scalar(stmt)
            session.close()
            if task:
                return jsonify(task.to_dict()), 200

    def update_task(self, id: int) -> Tuple[Response, int]:
        if request.method == 'PUT':
            params: dict = request.json
            session: Session = super().get_session()
            stmt = update(Task).where(Task.id == id).values(**params)
            session.execute(stmt)
            session.commit()
            task = session.query(Task).get(id)
            session.close()
            return jsonify(task.to_dict()), 200

    def delete_task(self, id: int) -> Tuple[Response, int]:
        if request.method == 'DELETE':
            session: Session = super().get_session()
            stmt = delete(Task).where(Task.id == id)
            session.execute(stmt)
            session.commit()
            session.close()
            return jsonify({"message": "Task was delete"}), 200

    def set_urls(self) -> None:
        self.tasks_bp.add_url_rule(
            '/<int:id>', view_func=self.update_task, methods=['PUT']
        )
        self.tasks_bp.add_url_rule(
            '/<int:id>', view_func=self.delete_task, methods=['DELETE']
        )
        self.tasks_bp.add_url_rule(
            '/<int:id>', view_func=self.get_task, methods=['GET']
        )
        self.tasks_bp.add_url_rule(
            '/', view_func=self.create_task, methods=['POST']
        )
        self.tasks_bp.add_url_rule(
            '/', view_func=self.get_tasks, methods=['GET']
        )


tasks_bp = TasksBlueprint().tasks_bp
