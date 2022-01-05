# CleanLeave

Automatically remove user join messages when the user leaves the server.

## Installation

You will need to install `poetry` to run this bot locally for development, but running in docker is preferred for production deployment.

Poetry can be installed using the following command:

- Windows: `py -3 -m pip install poetry`.
- Linux/Mac: `python3 -m pip install poetry`.

To install the dependencies you can then run `poetry install` in the folder you cloned the repository to.

You need to copy `.env.example` to `.env` and fill in the appropriate values.

To run the bot run `poetry run task start` or `docker-compose up` to run with docker.
