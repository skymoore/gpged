# Makefile

.PHONY: sdist publish install

default: build

build:
	@echo "Building..."
	pyinstaller gpged/__main__.py --collect-all gpged --hidden-import sip --onefile --name gpged --windowed --target-arch arm64

build-x86:
	pyinstaller gpged/__main__.py --collect-all gpged --hidden-import sip --onefile --name gpged.x86_64 --windowed	--target-arch x86_64

build-debug:
	@echo "Building..."
	pyinstaller gpged/__main__.py --collect-all gpged --hidden-import sip --onefile --name gpged --console --target-arch arm64

clean:
	@echo "Cleaning..."
	rm -rf build dist

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

install-pyqt5:
	@echo "Installing PyQt5..."
	cp -r /opt/homebrew/opt/pyqt@5/lib/python3.11/site-packages/* venv/lib/python3.11/site-packages

lock:
	@echo "Locking dependencies..."
	pipenv lock