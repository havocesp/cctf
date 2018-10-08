# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

import cctf

classifiers = [
    'Development Status :: 5 - Production',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

requirements = list()

requirements_path = os.path.join(os.getcwd(), 'requirements.txt')

if os.path.isfile(requirements_path):
    with open(requirements_path) as fp:
        requirements = fp.readlines()

exclude = ['.idea*', 'build*', '{}.egg-info*'.format(__package__), 'dist*', 'venv*', 'doc*', 'lab*']

setup(
    name=cctf.__project__,
    version=cctf.__version__,
    packages=find_packages(exclude=exclude),
    packages_dir={'': cctf.__package__},
    url=cctf.__site__,
    license=cctf.__license__,
    author=cctf.__author__,
    author_email=cctf.__email__,
    description=cctf.__description__,
    keywords=cctf.__keywords__,
    classifiers=classifiers,
    install_requires=requirements
)
