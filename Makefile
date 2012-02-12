.PHONY: init test lint coverage clean env

init: env
	@echo
	@echo "[INFO] use \`source activate\` to activate Python environment"

test: clean
	py.test -s --tb=short test

lint:
	find . -name "*.py" -not -path "./venv/*" | while read filepath; do \
		pep8 --ignore=E261 $$filepath; \
		pyflakes $$filepath; \
		pylint --reports=n --include-ids=y $$filepath; \
	done

coverage: clean
	# option #1: figleaf
	find *.py test -name "*.py" > coverage.lst
	figleaf `which py.test` test
	figleaf2html -f coverage.lst
	# option #2: coverage
	coverage run `which py.test` test
	coverage html
	# reports
	coverage report
	@echo "[INFO] additional reports in \`html/index.html\` (figleaf) and" \
			"\`htmlcov/index.html\` (coverage)"

clean:
	find . -name "*.pyc" | xargs rm || true
	rm -rf html .figleaf coverage.lst # figleaf
	rm -rf htmlcov .coverage # coverage
	rm -rf test/__pycache__ # pytest

env:
	virtualenv --no-site-packages venv
	ln -s venv/bin/activate
	$$SHELL -c '. venv/bin/activate; pip -E venv install -U flask PyYAML pytest' # TODO: should use setup.py
