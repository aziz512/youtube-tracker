.ONESHELL:
.PHONY: all purge clean run test coverage

# Set CAPTURE to false to see print statments for tests
CAPTURE ?= true

# Set FETCH_TEST to true to run tests that connect to the internet.
# This needs to be true for accurate coverage reports
FETCH_TEST ?= false

all: virtualenv

virtualenv:
	virtualenv virtualenv
	. virtualenv/bin/activate
	pip install flask
	pip install flask-cors
	pip install pytest
	pip install coverage
	pip install feedparser
	pip install yt-dlp
	pip install aioflask

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
