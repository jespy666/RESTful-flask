REVISION_CMD = alembic revision --autogenerate -m

.PHONY: migrations run

migrations:
	$(REVISION_CMD) "$(shell read -p 'Enter migration name: ' msg; echo $$msg)"

migrate:
	alembic upgrade head

api:
	python3 api.py

test:
	python3 -m unittest discover

install:
	pip install --no-cache-dir -r requirements.txt