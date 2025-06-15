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