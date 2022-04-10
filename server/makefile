.ONESHELL:
.PHONY: all purge clean run test coverage

CAPTURE ?= true

all: virtualenv

virtualenv:
	virtualenv virtualenv
	. virtualenv/bin/activate
	pip install flask
	pip install pytest
	pip install coverage
	pip install feedparser

purge: clean
	-rm -r virtualenv

clean:
	-rm .coverage
	-find . -path ./virtualenv -prune \
		-o -type d -name __pycache__ -print \
		-o -type d -name .pytest_cache -print \
	| while read line; do \
		echo Removing: "$$line";
		rm -r -- "$$line";
	done

run:
	. virtualenv/bin/activate
	flask run

test:
	. virtualenv/bin/activate
	if [ $(CAPTURE) = false ]; then
		coverage run -m pytest -s tests
	else
		coverage run -m pytest tests
	fi

coverage:
	. virtualenv/bin/activate
	coverage report -m --omit 'tests/*'
