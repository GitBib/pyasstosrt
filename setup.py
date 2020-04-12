#!/usr/bin/env python3

import os
from io import open

from setuptools import find_packages, setup


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, encoding="utf-8") as handle:
        return handle.read()


version = __import__("pyasstosrt").__version__

setup(
    name="pyasstosrt",
    version=version,
    description="Convert ASS subtitle to SRT format",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author="Ivan Vyalov",
    author_email="me@bnff.website",
    url="https://github.com/GitBib/pyasstosrt",
    download_url='https://github.com/GitBib/pyasstosrt/archive/{}.zip'.format(
        version
    ),
    license="Apache License, Version 2.0, see LICENSE file",
    packages=find_packages(exclude=["tests", "testapp"]),
    install_requires=['setuptools'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
