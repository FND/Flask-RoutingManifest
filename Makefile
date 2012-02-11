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

coverage:
	find app_pkg -name "*.py" > coverage.lst
	rm -rf html .figleaf
	figleaf `which py.test` test
	figleaf2html -f coverage.lst

clean:
	find . -name "*.pyc" | xargs rm || true
	rm -rf html .figleaf coverage.lst
	rm -rf test/__pycache__

env:
	virtualenv --no-site-packages venv
	ln -s venv/bin/activate
	$$SHELL -c '. venv/bin/activate; pip -E venv install -U flask PyYAML pytest' # TODO: should use setup.py
