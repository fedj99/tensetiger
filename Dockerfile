### GLOBAL ARGUMENTS

# Keep these in sync with project structure
ARG APP_SOURCE=app
ARG API_SOURCE=api

ARG APP_WORKDIR=/usr/local/src
ARG API_WORKDIR=/srv

# Keep these in sync with Vue build dir and Flask static dir
ARG BUILD_OUTPUT_DIR=${APP_WORKDIR}/dist
ARG STATIC_DIR=${API_WORKDIR}/static


### STAGE 1: BUILD

FROM node:18 AS build

# Inherit variables from global scope
ARG APP_SOURCE
ARG APP_WORKDIR

# Install additional build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y tree

WORKDIR ${APP_WORKDIR}

# Build Vue app
COPY ${APP_SOURCE} .
RUN npm install
RUN npm run build


### STAGE 2: DEPLOY

FROM python:3.10 AS deploy

# Inherit variables from global scope
ARG API_SOURCE
ARG API_WORKDIR
ARG STATIC_DIR
ARG BUILD_OUTPUT_DIR

# Install additional runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y tree

WORKDIR ${API_WORKDIR}

# Copy api folder
COPY ${API_SOURCE} .
# Copy app build files to static files
COPY --from=build ${BUILD_OUTPUT_DIR} ${STATIC_DIR}
# Install python dependencies
RUN pip install -r requirements.txt

# # Run app with gunicorn
# EXPOSE 80
# CMD ["gunicorn", "--bind", "0.0.0.0:80", "run:app"]
