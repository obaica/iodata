#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import glob
import subprocess
import Cython.Build
import numpy as np
from setuptools import setup
from distutils.extension import Extension


# Try to get the version from git describe
__version__ = '0.1.0'
try:
    print('Trying to get the version from git describe')
    git_describe = subprocess.check_output(["git", "describe", "--tags"])
    version_words = git_describe.decode('utf-8').strip().split('-')
    __version__ = version_words[0]
    if len(version_words) > 1:
        __version__ += '.post' + version_words[1]
    print('Version from git describe: {}'.format(__version__))
except (subprocess.CalledProcessError, OSError):
    pass

# Interact with version.py
fn_version = os.path.join(os.path.dirname(__file__), 'iodata', 'version.py')
version_template = """
# Do not edit this file, versioning is governed by ``git describe --tags`` and ``setup.py``.
__version__ = '{}'
"""
if __version__ is None:
    print('Trying to get the version from {}',format(fn_version))
    # Try to load the git version tag from version.py
    try:
        with open(fn_version, 'r') as fh:
            __version__ = fh.read().split('=')[-1].replace('\'', '').strip()
    except IOError:
        print('Could not determine version. Giving up.')
        sys.exit(1)
    print('Version according to {}: {}'.format(fn_version, __version__))
else:
    # Store the git version tag in version.py
    print('Writing version to {}'.format(fn_version))
    with open(fn_version, 'w') as fh:
        fh.write(version_template.format(__version__))


setup(
    name='iodata',
    version=__version__,
    description='',
    author='Toon Verstraelen',
    author_email='Toon.Verstraelen@UGent.be',
    url='https://github.com/theochem/iodata',
    package_dir={'iodata': 'iodata'},
    packages=['iodata', 'iodata.test'],
    cmdclass={'build_ext': Cython.Build.build_ext},
    ext_modules=[Extension(
        "iodata.overlap_accel",
        sources=['iodata/overlap_accel.pyx'],
        depends=['iodata/overlap_accel.pxd'],
        include_dirs=[np.get_include()],
    )],
    include_package_data=True,
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Intended Audience :: Science/Research',
    ],
    requires=['numpy', 'scipy', 'setuptools', 'distutils', 'Cython'],
    )