import re
import setuptools
import sys

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="speckle",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="Speckle Works",
    author_email="devops@speckle.works",
    description="A Python client for Speckle servers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/specklworks/pyspeckle",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent"
    ],
)
