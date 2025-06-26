.PHONY: install
install:
	poetry install
	poetry run pre-commit install

.PHONY: pre-commit
pre-commit:
	poetry run pre-commit uninstall
	poetry run pre-commit install

.PHONY: migrate
migrate:
	poetry run python manage.py migrate

.PHONY: makemigrations
makemigrations:
	poetry run python manage.py makemigrations

.PHONY: run-server
run-server:
	poetry run python manage.py runserver
