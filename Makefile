PYTHON = python3
PYTEST = $(PYTHON) -m pytest
UNIT_TESTS_DIR = tests/unit
SRC_DIR = src
LINTER = ruff
FORMATTER = black
TYPE_CHECKER = mypy

test:
	PYTHONPATH=$(SRC_DIR) $(PYTEST) $(UNIT_TESTS_DIR)

format:
	$(FORMATTER) $(SRC_DIR) $(UNIT_TESTS_DIR)

lint:
	$(LINTER) check $(SRC_DIR) $(UNIT_TESTS_DIR)

type-check:
	$(TYPE_CHECKER) $(SRC_DIR)

check: format lint type-check test

test-cov:
	PYTHONPATH=$(SRC_DIR) $(PYTEST) --cov=$(SRC_DIR) --cov-report=term-missing $(UNIT_TESTS_DIR)