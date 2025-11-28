.PHONY: build up down migrate seed test fmt lint help

help:
	@echo "Available commands:"
	@echo "  make build    - Build Docker images"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make migrate  - Run database migrations"
	@echo "  make seed     - Seed database with test data"
	@echo "  make test     - Run backend tests"
	@echo "  make fmt      - Format backend code (black, isort)"
	@echo "  make lint     - Lint backend code"
	@echo "  make clean    - Remove containers and volumes"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

migrate:
	docker compose exec backend alembic upgrade head

seed:
	docker compose exec backend python -m app.seeds.main

test:
	docker compose exec backend pytest -v

fmt:
	docker compose exec backend black app tests
	docker compose exec backend isort app tests

lint:
	docker compose exec backend black --check app tests
	docker compose exec backend isort --check app tests
	docker compose exec backend flake8 app tests

clean:
	docker compose down -v
	docker system prune -f

logs:
	docker compose logs -f

