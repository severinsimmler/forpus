#!/usr/bin/env python3

import io
import os
import sys
from shutil import rmtree
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

class UploadCommand(Command):
    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')
        
        sys.exit()

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
    ],
    # $ setup.py publish support
    cmdclass={
        'upload': UploadCommand,
    },
)
