.PHONY: dev-api
dev-api: export FLASK_CONFIG = development
dev-api: export FLASK_DB_PASSWORD = root
dev-api:
	cd api && flask run --debug

.PHONY: dev-app
dev-app:
	cd app && npm run dev

.PHONY: dev
dev:
	make dev-api &
	make dev-app
	fg

.PHONY: install-api
install-api:
	cd api && pip install -r requirements.txt

.PHONY: install-app
install-app:
	cd app && npm install

.PHONY: install
install:
	make install-api &
	make install-app
	fg
