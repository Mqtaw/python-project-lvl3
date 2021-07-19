install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader
	poetry run flake8 tests

test:
	env PYTHONPATH=. poetry run pytest tests -vv

test1:
	env PYTHONPATH=. poetry run pytest tests/test_1.py -vv

test-cov:
	env PYTHONPATH=. poetry run pytest --cov page_loader tests/ --cov-report xml

test-c:
	poetry run pytest --cov page_loader


try:
	poetry run page_loader https://ru.code-basics.com/

try1:
	poetry run page_loader https://ru.hexlet.io/programs

try2:
	poetry run page_loader https://page-loader.hexlet.repl.co

