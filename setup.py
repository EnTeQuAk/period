import os

setupargs = {}
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='period',
    version='0.1',
    description='Python date/time/duration/recurring string parser.',
    long_description='',
    author='Christopher Grebs',
    author_email='cg@webshox.org',
    url='',
    packages=['period'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
    install_requires=['pytz'],
    license='ISC',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ),
)
