from distutils.core import setup
import glob
import re
import os
import sys
import py2exe

py2exe_options = dict(
    ascii=True,
    excludes=['_ssl',  # Exclude _ssl
              'pyreadline', 'difflib', 'doctest', 'locale', 'pdb','unittest','inspect',
              'codecs', 'pydoc',#'threading','subprocess','sre_parse','weakref','ntpath','sre_compile','traceback',
              'optparse', 'pickle', 'calendar'],  # Exclude standard library
    dll_excludes=['msvcr71.dll'],  # Exclude msvcr71
    optimize=1,
    compressed=True,
    bundle_files=True
    )

setup(
    console = [{'script': 'PowerAnalyzer.py'}],
    options = {'py2exe': py2exe_options},
    zipfile = None
)
