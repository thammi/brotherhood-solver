#!/usr/bin/env python3

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "brotherhood solver",
    version = "0.1.0",
    author = "Thammi",
    author_email = "thammi@chaossource.net",
    description = ("Cross plattform client for Captcha Brotherhood"),
    license = "GPLv3",
    keywords = "captcha",
    url = "https://github.com/thammi/brotherhood-solver",
    packages=['brothersolver'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
    ],
    entry_points={
        'console_scripts': [
            'brotherhood_solver = brothersolver.gui:main',
            ],
        },
)

