
migrate:
	alembic upgrade head

api:
	python3 api.py

test:
	python3 -m unittest discover