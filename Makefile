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

test-cov:
	env PYTHONPATH=. poetry run pytest --cov page_loader tests/ --cov-report xml

try:
	poetry run page_loader https://ru.code-basics.com/

try1:
	poetry run page_loader https://ru.hexlet.io/programs

try2:
	poetry run page_loader https://page-loader.hexlet.repl.co

tryf:
	poetry run page_loader /home/mqtaw/python-project-lvl3/var/example/%D0%9A%D1%83%D1%80%D1%81%D1%8B%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8E%20%D0%A5%D0%B5%D0%BA%D1%81%D0%BB%D0%B5%D1%82.html

