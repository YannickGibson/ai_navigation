# Contains commands that come in handy when developing.

test:
	pytest .

test-cov:
	pytest --cov=. --cov-report=html .

format:
	ruff format

lint:
	ruff check