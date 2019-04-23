default: all

.PHONY: all
all: lint test mypy

.PHONY: lint
lint:
	python3 -m pylint ./*.py
	python3 -m pylint ./tests/*.py

.PHONY: test
test:
	./bin/run_tests.sh

.PHONY: mypy
mypy:
	./bin/run_mypy.sh
