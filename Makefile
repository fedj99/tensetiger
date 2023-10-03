.PHONY: dev-api
dev-api: export FLASK_CONFIG = development
dev-api: export FLASK_DB_PASSWORD = root
dev-api:
	cd api && flask run --debug
