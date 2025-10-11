format:
	isort .
	black .
	ruff check . --fix

lint:
	ruff check .
	isort . --check-only
	black . --check

