## RESTful-flask

A simple RESTful-api in Flask representing interaction with a todo list (CRUD)

### Stack  
![Static Badge](https://img.shields.io/badge/Flask-3.0.3-blue?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/Flask%20RESTful-0.3.10-purple?style=for-the-badge)  
![Static Badge](https://img.shields.io/badge/SQLAlchemy-2.0.30-green?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/Alembic-1.13.1-red?style=for-the-badge)  
### How to run
* clone repo `git clone https://github.com/jespy666/RESTful-flask.git`
* go to project dir `cd RESTful-flask`
* create virtual env `python3 -m venv venv`
* activate venv `source venv/bin/activate`
* create and fill .env `touch .env` (see .env.example)
#### By CLI:
* install dependencies `make install`
* apply migrations `make migrate`
* run api `make api`
#### By Docker
* setup ENV in `.env` to 'prod'
* run `docker-compose up -d`
* explore
