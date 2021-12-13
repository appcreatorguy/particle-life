#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0']

setup(
    author="Manas Mengle",
    author_email='manmenonsense@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="A game of life with particles",
    entry_points={
        'console_scripts': [
            'particle_life=particle_life.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT License",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='particle_life',
    name='particle_life',
    packages=find_packages(include=['particle_life', 'particle_life.*']),
    url="https://github.com/appcreatorguy/particle-life",
    version='0.0.1',
    zip_safe=False,
)
