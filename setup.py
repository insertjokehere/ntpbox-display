#!/usr/bin/env python

from setuptools import setup, find_packages
import os
import codecs

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()

setup(
    name='ntpbox_display',
    version='0.1dev1',
    packages=find_packages(),
    license='MIT',
    description="",
    #long_description=read('README.rst'),
    install_requires=read('requirements.txt').split(),
    author="Will Hughes",
    author_email="will@willhughes.name",
    url="https://github.com/insertjokehere/ntpbox-display",
    entry_points={
        'console_scripts': [
            'ntpbox-display = ntpbox_display:App.main',
        ]
    },
    classifiers=[
    ]
)
