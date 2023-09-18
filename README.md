# Transport Management App Example

Build with [FastAPI](https://fastapi.tiangolo.com/) and [PostgreSQL](https://www.postgresql.org/) app that lets you manage rides that people can book to travel.

## Prerequisites

- [Python 3](https://www.python.org/), v. 10+ or latest (recommended),
- [Docker](https://www.docker.com/) with [Docker Compose](https://docs.docker.com/compose/),
- Have set up an email address that will enable you sending emails through SMTP server.

## Setting Up Environmental Variables

Before you dive in, you need to set up project environmental variables.
- Open the project directory,
- Create an ***.env*** file in the root directory (/transport-app/),
- Paste below content with your custom envs:

```python
MAIL_USERNAME = <username> # can be an email address or a full name - check your email settings
MAIL_PASSWORD = <password> # your email password
MAIL_FROM = <email> # an email address
MAIL_PORT = 587 # should be fine - check your email SMTP server
MAIL_SERVER = <server> # SMTP server, for example outlook emails might have: smtp.office365.com

SECRET_KEY = <secret> - # run $ openssl rand -hex 32 in a terminal and paste the result
ALGORITHM = <algorithm> - # will be needed to hash users passwords. I used HS256 for development
ACCESS_TOKEN_EXPIRE_MINUTES = 30 - # minutes after the access token will be expired. Can leave as it is
```

## Running The App

1. Have your Docker running
2. Go to the root project directory (/transport-app/)
3. Run the following command in the terminal and wait:
```bash
$ docker-compose up --build
```
4. Go to http://localhost:8008/docs and use the app

## Documentation

- [Swagger docs](http://localhost:8008/docs)
- [Redocly docs](http://localhost:8008/redoc)
- Whole project is well documented via pythonic docstrings. You can access docs through [pydoc](https://docs.python.org/3/library/pydoc.html)

## Testing The App

To run tests, type inside of web container:
```bash
pytest
```

## Design Patterns

TBD
