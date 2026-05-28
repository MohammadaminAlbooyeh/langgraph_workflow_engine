.PHONY: install run test lint clean docker-build docker-up

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio pytest-cov ruff mypy

run:
	uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

run-frontend:
	cd frontend && npm start

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=backend --cov-report=term --cov-report=html

lint:
	ruff check backend/

typecheck:
	mypy backend/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache htmlcov .coverage

docker-build:
	docker build -t langgraph-workflow-engine:latest .

docker-build-all:
	docker build -t langgraph-workflow-engine:latest .
	docker build -f Dockerfile.dashboard -t langgraph-workflow-dashboard:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

db-init:
	python scripts/init_db.py

db-seed:
	python scripts/seed_data.py

all: install test lint
