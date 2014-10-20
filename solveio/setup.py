#! /usr/bin/env python


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="solveio",
    version="0.1",
    description=("Framework used to handle and check solutions"),
    long_description=open("README.md").read(),
    author="Alexandru Coman, Claudiu Popa, Cosmin Poieana",
    author_email=(
        "Alexandru Coman <alex@ropython.org>, "
        "Claudiu Popa <claudiu@ropython.org>, "
        "Cosmin Poieana <cmin@ropython.org>"
    ),
    url="https://github.com/RoPython/ropython-challenge/tree/master/solveio",
    packages=["solveio", "solveio.api", "solveio.problems"],
    scripts=["scripts/solveio"],
    requires=["redis", "cherrypy"]
)
