#!/usr/bin/env python3

import os, sys
from setuptools import find_packages, setup


def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with open(filename, encoding="utf-8", mode="rt") as fp:
        return fp.read()


with open("./README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Sky Moore",
    author_email="i@msky.me",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
    ],
    description="GUI for encrypting and decrypting text with GPG.",
    include_package_data=True,
    keywords=["gpg"],
    license="MIT",
    long_description_content_type="text/markdown",
    long_description=readme,
    name="gpg-encrypt-decrypt-gui",
    packages=find_packages(include=["gpged"]),
    entry_points={"gui_scripts": ["gpged = gpged.__main__:main"]},
    url="https://github.com/skymoore/gpged",
    version="v0.0.1",
    zip_safe=True,
)
