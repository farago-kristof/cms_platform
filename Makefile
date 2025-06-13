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

rm-pg-volume:
	@echo "Removing db volume"
	docker compose down
	docker volume rm cms-platform_pg_data

up:
	docker compose up -d postgres
	@echo "Waiting for Postgres to be ready..."
	@until docker exec -it cms-platform-postgres-1 pg_isready -U postgres; do \
		echo "Postgres is unavailable - sleeping"; \
		sleep 2; \
	done
	@echo "Postgres is ready, starting other services..."
	docker compose up --build