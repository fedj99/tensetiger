.PHONY: dev
dev: export FLASK_CONFIG = development
dev:
	flask --app api/main run --debug
