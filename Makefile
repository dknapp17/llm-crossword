# ---------- Variables ----------
PYTHONPATH=PYTHONPATH=.

# ---------- Test ----------
test:
	$(PYTHONPATH) uv run python -m unittest discover tests

test-file:
	$(PYTHONPATH) uv run python -m unittest $(FILE)

# Example:
# make test-file FILE=tests/test_solvers.py


# ---------- Lint ----------
lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

format:
	uv run ruff format .


# ---------- App ----------
app:
	$(PYTHONPATH) uv run streamlit run app/streamlit_app.py


# ---------- Combined ----------
check: lint test