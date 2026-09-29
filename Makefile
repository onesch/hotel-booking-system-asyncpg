dev:
	uv run uvicorn app.main:app --reload

cov:
	uv run pytest --cov=app --cov-report=term-missing

test:
	uv run pytest -vv
