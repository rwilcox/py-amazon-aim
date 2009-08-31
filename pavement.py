import os
import sys

from paver.easy import *
from paver.setuputils import setup
from setuptools import find_packages

# import here packages only needed for development
try:
    from paver.virtual import bootstrap
except:
    pass

try:
    from github.tools.task import *
except:
    pass
    

version = "0.1.0"

long_description = open('README.rst', 'r').read()

classifiers = [
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    "Programming Language :: Python",
    ]

install_requires = [
    'setuptools',
    ]

entry_points="""
    # -*- Entry points: -*-
    """

setup(
    name='py-amazon-aim',
    version=version,
    description='A Python implementation of the Amazon Inventory Management (AIM) API',
    long_description=long_description,
    classifiers=classifiers,
    keywords='',
    author='Ryan Wilcox',
    author_email='rwilcox@wilcoxd.com',
    url='',
    license='GPL',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages=[],
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
    install_requires=install_requires,
    entry_points=entry_points,
    )

options(
    virtualenv=Bunch(
        script_name='bootstrap.py',
        dest_dir='./virtual-env/',
        packages_to_install=[
            'virtualenv',
            'github-tools',
            'Nose'
            ]
        ),
    sphinx=Bunch(
        docroot='docs',
        builddir='build',
        sourcedir='source',
        ),
    )

@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""