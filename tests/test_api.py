import unittest

from sqlalchemy import func

from tests.test_setup import AppTestCase
from tests.fixture_loader import load_fixtures

from src.tasks.models import Task

from config import BASE_DIR


class TestGetTasks(AppTestCase):

    def test_fetch_all_tasks(self) -> None:
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(
            response.headers['Content-Type'],
            'application/json'
        )

    def test_success_get_task(self) -> None:
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'Task 1')
        self.assertEqual(
            response.headers['Content-Type'],
            'application/json'
        )

    def test_get_non_existed_task(self) -> None:
        response = self.app.get('/tasks/999')
        self.assertEqual(response.json['error'], 'task does not exist')
        self.assertEqual(
            response.headers['Content-Type'],
            'application/json'
        )
        self.assertEqual(response.status_code, 200)


class TestCreateTask(AppTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.created_cases = load_fixtures(
            f'{BASE_DIR}/tests/fixtures/create.json'
        )

    def test_success_create_task(self) -> None:
        data = self.created_cases['valid']
        response = self.app.post('/tasks', json=data)
        session = self.session_factory.get_session()
        self.assertEqual(session.query(func.count(Task.id)).scalar(), 4)
        session.close()
        self.assertEqual(response.status_code, 200)

    def test_create_with_empty_body(self) -> None:
        data = self.created_cases['empty']
        response = self.app.post('/tasks', json=data)
        self.assertEqual(response.json['error'], "validation error")
        session = self.session_factory.get_session()
        self.assertEqual(session.query(func.count(Task.id)).scalar(), 3)
        session.close()
        self.assertEqual(response.status_code, 200)

    def test_create_existed_task(self) -> None:
        data = self.created_cases['existed']
        response = self.app.post('/tasks', json=data)
        session = self.session_factory.get_session()
        self.assertEqual(session.query(func.count(Task.id)).scalar(), 3)
        session.close()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json['error'],
            'task with that title are already exists'
        )


class TestUpdateTask(AppTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.updated_cases = load_fixtures(
            f'{BASE_DIR}/tests/fixtures/update.json'
        )

    def test_success_update(self) -> None:
        data = self.updated_cases['valid']
        response = self.app.put('/tasks/2', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], "valid name")
        self.assertEqual(
            response.json['description'],
            "New description"
        )

    def test_update_with_empty_fields(self) -> None:
        data = self.updated_cases['empty']
        response = self.app.put('/tasks/2', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['error'], 'validation error')

    def test_update_non_existent_task(self) -> None:
        data = self.updated_cases['not_exist']
        response = self.app.put('/tasks/999', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['error'], 'task does not exist')


class TestDeleteTask(AppTestCase):

    def test_success_delete(self) -> None:
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Task was delete')
        session = self.session_factory.get_session()
        self.assertEqual(session.query(func.count(Task.id)).scalar(), 2)
        session.close()

    def test_delete_non_existent_task(self) -> None:
        response = self.app.delete('/tasks/999')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['error'], 'task does not exist')


class TestEmptyTasks(AppTestCase):

    def setUp(self) -> None:
        super().setUp()
        if self.is_filled():
            self.clean_db()

    def test_get_all_tasks_from_empty_db(self) -> None:
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])


if __name__ == '__main__':
    unittest.main()
