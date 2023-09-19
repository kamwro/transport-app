# Transport Management App Example

Build with [FastAPI](https://fastapi.tiangolo.com/) and [PostgreSQL](https://www.postgresql.org/) backend app that lets you manage rides that people can book to travel.

## Prerequisites

- [Python 3](https://www.python.org/), v. 10+ or latest (recommended),
- [Docker](https://www.docker.com/) with [Docker Compose](https://docs.docker.com/compose/),
- have set up an email address that will enable you sending emails through SMTP server,
- have prepared different email address to do tests, if you wish.

## Cloning The Repository

```bash
$ git clone https://github.com/kamwro/transport-app
```

## Setting Up Environmental Variables

Before you dive in, you need to set up project environmental variables.
1. Open the project directory
2. Create an ***.env*** file in the root directory (/transport-app/)
3. Paste below content with your custom envs:

```python
# email sending messages
MAIL_USERNAME = <username> # can be an email address or a full name - check your email settings
MAIL_PASSWORD = <password> # your email password
MAIL_FROM = <email> # an email address
MAIL_PORT = 587 # should be fine - check your email SMTP server
MAIL_SERVER = <server> # SMTP server, for example outlook emails might have: smtp.office365.com

# this will be used for tests and must be a valid email addresses
TEST_MAIL = <mail>

# token and authentication stuff
SECRET_KEY = <secret> # run $ openssl rand -hex 32 in a terminal and paste the result
ALGORITHM = <algorithm> # will be needed to hash users passwords. I used HS256 for development
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # minutes after the access token will be expired. Can leave as it is
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

- [Swagger docs](http://localhost:8008/docs),
- [Redocly docs](http://localhost:8008/redoc),
- access [pdoc](https://pdoc.dev/) documentation in the ./docs folder,
- whole project is well documented via pythonic docstrings. You can also access docs through [pydoc](https://docs.python.org/3/library/pydoc.html).

## Testing The App

Unit tests conducted using [pytest](https://docs.pytest.org/en/7.4.x/), FastAPI [TestClient](https://fastapi.tiangolo.com/tutorial/testing/) and [SQLite](https://www.sqlite.org/index.html) in-memory database.

To run tests, type inside of web container:
```bash
$ pytest
```

## Design Patterns And Clean Code

Building my app, I've been trying to achieve clean code principles, such as:

- hide the instantiation process from the user,
- simple is better than complex and complex is better than complicated,
- readability is crucial,
- Do not Repeat Yourself (as possible),
- stay true to the Single Responsibility principle.

Some of the design patterns used in my project:

- ***iterators*** - mostly dictionaries, JSON responses,
- ***dependency injections*** - user authentication, admin priviliges, get_db etc.,
- ***facade*** - given by FastAPI docs and by structuring project files.

## Feedback

More than welcome!

## License 

[MIT](https://github.com/kamwro/transport-app/blob/main/LICENSE)
