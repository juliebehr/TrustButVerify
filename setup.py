from __future__ import print_function

import os
import sys
import shutil
import tempfile
import subprocess
from distutils.ccompiler import new_compiler
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

try:
    import numpy
except ImportError:
    print('Building and running mdtraj requires numpy', file=sys.stderr)
    sys.exit(1)



##########################
VERSION = "0.0.1"
ISRELEASED = False
__version__ = VERSION
##########################


CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)
Programming Language :: C
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Scientific/Engineering :: Bio-Informatics
Topic :: Scientific/Engineering :: Chemistry
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""

################################################################################
# Writing version control information to the module
################################################################################

def git_version():
    # Return the git revision as a string
    # copied from numpy setup.py
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = 'Unknown'

    return GIT_REVISION


def write_version_py(filename='trustbutverify/version.py'):
    cnt = """
# THIS FILE IS GENERATED FROM TrustButVerify SETUP.PY
short_version = '%(version)s'
version = '%(version)s'
full_version = '%(full_version)s'
git_revision = '%(git_revision)s'
release = %(isrelease)s

if not release:
    version = full_version
"""
    # Adding the git rev number needs to be done inside write_version_py(),
    # otherwise the import of numpy.version messes up the build under Python 3.
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    else:
        GIT_REVISION = 'Unknown'

    if not ISRELEASED:
        FULLVERSION += '.dev-' + GIT_REVISION[:7]

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'full_version': FULLVERSION,
                       'git_revision': GIT_REVISION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()


write_version_py()
setup(name='trustbutverify',
      author='Kyle A. Beauchamp',
      author_email='kyleabeauchamp@gmail.com',
      version=__version__,
      license='LGPLv2.1+',
      url="https://github.com/kyleabeauchamp/TrustButVerify",
      download_url = "https://github.com/kyleabeauchamp/TrustButVerify/releases/latest",
      platforms=['Linux', 'Mac OS-X', 'Unix', 'Windows'],
      classifiers=CLASSIFIERS.splitlines(),
      packages=["trustbutverify"],
      package_dir={'trustbutverify': 'trustbutverify'},
      package_data={'trustbutverify.datasets': ['datasets/*']},
    )
