# Makefile

.PHONY: sdist publish install

sdist:
	@echo "Building source distribution..."
	python3 -m build --sdist

publish: sdist
	@echo "Publishing to pypi..."
	@echo "Use PyPI api token for password!"
	twine upload dist/* -u __token__
	rm -rf dist

install:
	@echo "Installing..."
	python3 -m pip install .

lock:
	@echo "Locking dependencies..."
	pipenv lock