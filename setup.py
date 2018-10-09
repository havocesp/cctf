# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import cctf

classifiers = [
    'Development Status :: 5 - Production',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

exclude = ['.idea*', 'build*', '{}.egg-info*'.format(__package__), 'dist*', 'venv*', 'doc*', 'lab*']

setup(
    name=cctf.__project__,
    version=cctf.__version__,
    packages=find_packages(exclude=exclude),
    url=cctf.__site__,
    license=cctf.__license__,
    author=cctf.__author__,
    author_email=cctf.__email__,
    description=cctf.__description__,
    keywords=cctf.__keywords__,
    classifiers=classifiers,
    install_requires=cctf.__dependencies__,
    dependency_links=cctf.__deplinks__
)
