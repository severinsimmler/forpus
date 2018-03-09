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
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
    packages=['forpus'],
    install_requires=[
        'pandas>=0.21.1',
        'networkx>=2.0',
        'git+git://github.com/cophi-wue/metadata-toolbox.git'
        ]
    keywords=['corpora', 'text mining', 'natural language processing']
)
