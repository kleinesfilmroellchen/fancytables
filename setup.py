#!/usr/bin/env python3
from setuptools import setup, find_packages
from __init__ import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="fancytables",
    version=__version__,
    autor="kleinesfilmröllchen",
    description="Fancy table formatting that builds on prettytable",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kleinesfilmroellchen/fancytables",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ]
)
