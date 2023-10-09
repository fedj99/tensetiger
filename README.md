# Bring Brang Brung

A small web app to learn irregular verb forms effectively.

## Developer Guide

### Dependencies and Project Setup

The project requires the following to be installed on your computer:

- A recent version of python, `python>=3.10`
- A recent version of NodeJS, `node>=18.0 LTS` and NPM
- Optionally, Docker, if you want to contribute to app deployment
- Optionally, any python virtual environment manager, e.g. `virtualenv`, `venv`,
  `conda`, `mamba` or `micromamba`. Only if you don't want to install
  dependencies to your system python.

### Frontend (`./app`)

#### Development

The first time you clone the project, you need to install NPM dependencies.

```sh
cd app
npm install
```

Then simply run

```sh
npm run dev
```

to start a local development server. Do not use this in production. To make a
static build (the frontend is an SPA that needs to be compiled to static
HTML/JS), run

```sh
npm run build
```

### Backend (`./api`)

#### Development

First, install python dependencies:

```sh
cd api
pip install -r requirements.txt
```

You need to set some environment variables. These can be defined in your shell,
but a better place is to put them in a `.env.local` file. This file is not
tracked by git. Complete the following tasks the first time you set up the
project:

- Generate authentication keys (for secure cookies), by running
  `scripts/generate_secret_key` and copy its output.
- Set up a local PostgreSQL server, or use a development database anywhere else

```ini
# .env.local
FLASK_ENV=development
FLASK_DEBUG=true
FLASK_SECRET_KEY=e2fde91d7b8f57919c5a1703325b2355a8632d27f27d41a051d8d7d1b65a1864
FLASK_DB_PASSWORD=[database password here]
```

The file `.env` contains common configuration for every mode. You can place
config-specific values in `.env.[mode]`, where `[mode]` is the same as the
`FLASK_ENV` you are using. Add `.local` (e.g. `.env.staging.local`) to ignore
the file in git (good for database passwords etc.)

Once you set up the database connection parameters (host, username, password),
you can use `flask` to run some database migrations. The `init-db` command wipes
and creates all necessary tables. Run:

```sh
flask init-db # WARNING: Will delete any tables with the same name
```

Then you can finally run the development server:

```sh
flask run
```

You don't need to build the API before deploying, but be aware that **you should
not use the Flask development server (i.e. `flask run`) when deploying to
production**. See [Deployment](#deployment) for more info

#### Adding New Routes

Generally, routes should be grouped in Flask blueprints. The
`api.blueprints.api` blueprint serves as an entry point for the API. It is
rooted under the `/api/` URL.

To add a new top-level blueprint, create a new file in `api/blueprints`, e.g.
`example.py`. Create your blueprint and name it e.g. `bp`. Then, in
`api/blueprints/__init__.py`, add the following:

```python
# Other imports
from .example import bp as example

__all__ = [
    # Other exports
    example
]
```

Then, in `api/__init__.py`, add the following lines in the app factory method:

```python
from api import blueprints

def create_app():
    # Other stuff
    app.register_blueprint(blueprints.example)
```

The process is similar for sub-routes. The important thing is to call
`register_blueprint` on all your blueprints.

## Deployment

The website is currently hosted on <https://render.com> on its free plan. It is
configured to use the docker image built from `./Dockerfile`.

### Docker

The docker image should contain everything required to run the server, that is,
it should be able to serve a python WSGI application. We use the `gunicorn`
python package as our production HTTP server of choice. This is all configured
in the provided Dockerfile. The build roughly performs the following tasks:

1. Set up build environment for VueJS frontend and build it
2. Copy API files and frontend files into a special directory of the API,
   `/frontend`. The API will relay any requests to non-existent routes to the
   frontend (which will have to handle 404's)
3. Set up python environment for the server, installing all dependencies.
4. Serve the application with `gunicorn`

Node build dependencies are not included in the final image (multistage build).

You can build the image locally with:

```sh
docker build -t b3 .
```

Render.com will automatically build and deploy the application when pushing to
the `main` branch.
