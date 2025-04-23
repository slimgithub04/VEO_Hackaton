.PHONY: help setup run test lint clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "make setup    - Create virtual environment and install dependencies"
	@echo "make run     - Run the Flask application"
	@echo "make test    - Run tests with pytest"
	@echo "make lint    - Run code linting"
	@echo "make clean   - Clean up generated files"
	@echo "make docker-build - Build Docker image"
	@echo "make docker-run   - Run with Docker Compose"

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	flask db upgrade

run:
	flask run

test:
	pytest tests/ --cov=. --cov-report=term-missing

lint:
	flake8 .
	black .
	isort .

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type f -name ".coverage" -delete

docker-build:
	docker-compose build

docker-run:
	docker-compose up