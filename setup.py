# -*- coding: utf-8 -*-
from pathlib import Path

from setuptools import setup, find_packages

import cctf

classifiers = [
    'Development Status :: 5 - Production',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

exclude = ['.idea*', 'build*', '{}.egg-info*'.format(__package__), 'dist*', 'venv*', 'doc*', 'lab*']
keywords = ['altcoins', 'altcoin', 'exchange', 'bitcoin', 'trading']
requirements_file = Path(__file__).parent.joinpath('requirements.txt')  # type: Path

if requirements_file.exists():
    dependencies = requirements_file.read_text().splitlines()
else:
    dependencies = list()

setup(
    name=cctf.__package__,
    version=cctf.__version__,
    packages=find_packages(exclude=exclude),
    url=cctf.__site__,
    license=cctf.__license__,
    author=cctf.__author__,
    author_email=cctf.__email__,
    description=cctf.__description__,
    keywords=keywords,
    classifiers=classifiers,
    install_requires=dependencies,
)
