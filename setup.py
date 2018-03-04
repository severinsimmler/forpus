#!/usr/bin/env python3

from setuptools import setup

setup(
    name='forpus',
    version='0.0.1.dev1',
    description='Converting plain text corpora to NLP-specific corpus formats.',
    # url
    author='Severin Simmler',
    author_email='severin.simmler@stud-mail.uni-wuerzburg.de',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
    packages=['forpus']
    # install_requires
    keywords=['corpora', 'text mining', 'natural language processing']
)
