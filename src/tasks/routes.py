from typing import Sequence, Any

from flask import request, jsonify, Response
from flask_restful import Resource

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from .models import Task
from ..session import SessionFactory
from .validators import validate_request_params


# routes for /tasks
class DirectTasks(Resource, SessionFactory):

    def __init__(self, **kwargs: Any) -> None:
        # provide Database URL for SQLAlchemy session
        db_url: str = kwargs.get('db_url')
        super().__init__(db_url=db_url)

    def get(self) -> Response:
        session: Session = super().get_session()
        # get all tasks
        stmt = select(Task)
        tasks: Sequence[Task] = session.scalars(stmt).all()
        session.close()
        return jsonify([task.to_dict() for task in tasks])

    @validate_request_params
    def post(self) -> Response:
        # get request body
        data: dict = request.json
        session: Session = super().get_session()
        try:
            stmt = select(Task).where(Task.title == data.get('title'))
            task: Task | None = session.scalar(stmt)
            # check if task with unique Title name existed
            if task:
                return jsonify({
                    "error": "task with that title are already exists"
                })
            new_task = Task(**data)
            session.add(new_task)
            session.commit()
            session.close()
            return jsonify(new_task.to_dict())
        finally:
            session.close()


# routes for /tasks/<id>
class ParametrizeTasks(Resource, SessionFactory):

    def __init__(self, **kwargs: Any) -> None:
        # provide Database URL for SQLAlchemy session
        db_url: str = kwargs.get('db_url')
        super().__init__(db_url=db_url)

    def get(self, task_id: int) -> Response:
        session: Session = super().get_session()
        try:
            # try to get task by id
            stmt = select(Task).where(Task.id == task_id)
            task: Task | None = session.scalar(stmt)
            # check if task exist
            if task:
                return jsonify(task.to_dict())
            return jsonify({"error": "task does not exist"})
        finally:
            session.close()

    @validate_request_params
    def put(self, task_id: int) -> Response:
        # get request body params
        params: dict = request.json
        session: Session = super().get_session()
        try:
            # try to find task by id
            stmt1 = select(Task).where(Task.id == task_id)
            task: Task | None = session.scalar(stmt1)
            # check if task exist
            if not task:
                return jsonify({"error": "task does not exist"})
            new_title = params.get('title')
            # check if title change
            if new_title:
                # try to find task with updated title
                stmt3 = select(Task).where(Task.title == new_title)
                existed_task: Task | None = session.scalar(stmt3)
                # send error message if task with that title existed
                if existed_task:
                    return jsonify({
                        "error": "task with that title are already exists"
                    })
            # update task fields
            stmt2 = update(Task).where(Task.id == task_id).values(**params)
            session.execute(stmt2)
            session.commit()
            return jsonify(task.to_dict())
        finally:
            session.close()

    def delete(self, task_id: int) -> Response:
        session: Session = super().get_session()
        try:
            # try to find task by id
            stmt1 = select(Task).where(Task.id == task_id)
            task: Task | None = session.scalar(stmt1)
            # check if task exist
            if not task:
                return jsonify({"error": "task does not exist"})
            # delete task
            stmt2 = delete(Task).where(Task.id == task_id)
            session.execute(stmt2)
            session.commit()
            return jsonify({"message": "Task was delete"})
        finally:
            session.close()
