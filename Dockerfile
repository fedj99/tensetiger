### GLOBAL ARGUMENTS

# Keep these in sync with project structure
ARG APP_SOURCE=app
ARG API_SOURCE=api

ARG APP_WORKDIR=/usr/local/src
ARG API_WORKDIR=/srv

# Keep these in sync with Vue build dir and Flask static dir
ARG BUILD_OUTPUT_DIR=${APP_WORKDIR}/dist
ARG STATIC_DIR=${API_WORKDIR}/frontend


### STAGE 1: BUILD

FROM node:lts AS build

# Inherit variables from global scope
ARG APP_SOURCE
ARG APP_WORKDIR

WORKDIR ${APP_WORKDIR}

# Build Vue app
COPY ${APP_SOURCE} .
RUN npm install \
	&& npm run build


### STAGE 2: DEPLOY

FROM python:3.11 AS deploy

# Needs to be set for gunicorn to find app
ENV PYTHONPATH=src
ENV FLASK_ENV=production
ENV FLASK_CONFIG=production
# Set the DB password as a secret in the deployment
# ENV FLASK_DB_PASSWORD=root
ENV GUNICORN_SERVER_PORT=8000

# Inherit variables from global scope
ARG API_SOURCE
ARG API_WORKDIR
ARG STATIC_DIR
ARG BUILD_OUTPUT_DIR

WORKDIR ${API_WORKDIR}

# First copy only requirements file and install dependencies (speed up docker build)
COPY ${API_SOURCE}/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy api folder
COPY ${API_SOURCE} .
# Copy app build files to static files
COPY --from=build ${BUILD_OUTPUT_DIR} ${STATIC_DIR}

# Run the web server
EXPOSE ${GUNICORN_SERVER_PORT}
CMD ["gunicorn"]
