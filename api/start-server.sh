#!/usr/bin/env sh

# Bind on all interfaces
flask --app api run --debug --host 0.0.0.0 --port "${SRV_PORT}"
