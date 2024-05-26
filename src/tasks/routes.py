from typing import Sequence, Any

from flask import request, jsonify, Response
from flask_restful import Resource

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from .models import Task
from ..session import SessionFactory
from .validators import validate_task


class DirectTasks(Resource, SessionFactory):

    def __init__(self, **kwargs) -> None:
        # provide Database URL for SQLAlchemy session
        db_url: str = kwargs.get('db_url')
        super().__init__(db_url=db_url)

    def get(self) -> Response:
        session: Session = super().get_session()
        stmt = select(Task)
        tasks: Sequence[Task] = session.scalars(stmt).all()
        session.close()
        return jsonify([task.to_dict() for task in tasks])

    def post(self) -> Response:
        data: dict = request.json
        session: Session = super().get_session()
        if not validate_task(data):
            return jsonify({"error": "validation error"})
        stmt = select(Task).where(Task.title == data.get('title'))
        task: Task | None = session.scalar(stmt)
        # check if task with unique Title name existed
        if task:
            return jsonify({"error": "task with that title are already exists"})  # noqa: E501
        new_task = Task(**data)
        session.add(new_task)
        session.commit()
        session.close()
        return jsonify(new_task.to_dict())


class ParametrizeTasks(Resource, SessionFactory):

    def __init__(self, **kwargs: Any) -> None:
        # provide Database URL for SQLAlchemy session
        db_url: str = kwargs.get('db_url')
        super().__init__(db_url=db_url)

    def get(self, task_id: int) -> Response:
        session: Session = super().get_session()
        stmt = select(Task).where(Task.id == task_id)
        task: Task | None = session.scalar(stmt)
        session.close()
        # check if task exist
        if task:
            return jsonify(task.to_dict())
        return jsonify({"error": "task does not exist"})

    def put(self, task_id: int) -> Response:
        params: dict = request.json
        if not validate_task(params):
            return jsonify({"error": "validation error"})
        session: Session = super().get_session()
        stmt1 = select(Task).where(Task.id == task_id)
        task: Task | None = session.scalar(stmt1)
        # check if task exist
        if not task:
            return jsonify({"error": "task does not exist"})
        stmt2 = update(Task).where(Task.id == task_id).values(**params)
        session.execute(stmt2)
        session.commit()
        session.close()
        return jsonify(task.to_dict())

    def delete(self, task_id: int) -> Response:
        session: Session = super().get_session()
        stmt1 = select(Task).where(Task.id == task_id)
        task: Task | None = session.scalar(stmt1)
        # check if task exist
        if not task:
            return jsonify({"error": "task does not exist"})
        stmt2 = delete(Task).where(Task.id == task_id)
        session.execute(stmt2)
        session.commit()
        session.close()
        return jsonify({"message": "Task was delete"})
