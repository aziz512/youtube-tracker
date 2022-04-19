.ONESHELL:
.PHONY: all purge clean run test coverage

all: virtualenv

virtualenv:
	python -m venv virtualenv
	. virtualenv/bin/activate
	pip install flask
	pip install flask-cors
	pip install pytest
	pip install coverage

purge: clean
	-rm -r virtualenv

clean:
	-rm -r app/__pycache__
	-rm -r tests/__pycache__
	-rm -r .pytest_cache
	-rm .coverage

run:
	. virtualenv/bin/activate
	flask run

test:
	. virtualenv/bin/activate
	coverage run -m pytest tests

coverage:
	. virtualenv/bin/activate
	coverage report -m
