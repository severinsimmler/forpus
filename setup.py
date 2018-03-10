#!/usr/bin/env python3

from setuptools import find_packages, setup, Command


NAME = 'forpus'
DESCRIPTION = 'Converts a plain text corpus into a NLP-specific corpus format.'
URL = 'https://github.com/severinsimmler/forpus'
EMAIL = 'severin.simmler@stud-mail.uni-wuerzburg.de'
AUTHOR = 'Severin Simmler'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.0.1'
REQUIRED = [
     'pandas>=0.21.1',
     'networkx>=2.0'
]

about = {}
about['__version__'] = VERSION

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=['forpus'],
    entry_points={
        'console_scripts': ['mycli=forpus:cli'],
    },
    install_requires=REQUIRED,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ]
)
