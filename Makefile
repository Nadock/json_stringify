default: all

.PHONY: all
all: lint test

.PHONY: lint
lint:
	python3 -m pylint ./*.py

.PHONY: test
test:
	python3 ./json_stringify_command_test.py
