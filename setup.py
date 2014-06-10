"""PDBFetcher: A simple python API for querying the RCSB PDB and 
downloading PDB files"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

DOCLINES = __doc__.split("\n")

import os
import sys
import tempfile
import shutil
import subprocess
from glob import glob
from distutils.version import StrictVersion
from distutils.command.build_scripts import build_scripts
from setuptools import setup
PY3 = sys.version_info >= (3,0)

#########################################
VERSION = "0.0.1"
ISRELEASED = False
__author__ = "Christian Schwantes"
__version__ = VERSION
########################################


def warn_on_version(module_name, minimum=None, package_name=None, recommend_conda=True):
    if package_name is None:
        package_name = module_name

    class VersionError(Exception):
        pass

    msg = None
    try:
        package = __import__(module_name)
        if minimum is not None:
            try:
                v = package.version.short_version
            except AttributeError:
                v = package.__version__
            if StrictVersion(v) < StrictVersion(minimum):
                raise VersionError
    except ImportError:
        if minimum is None:
            msg = 'pdbfetcher requires the python package "%s", which is not installed.' % package_name
        else:
            msg = 'pdbfetcher requires the python package "%s", version %s or later.' % (package_name, minimum)
    except VersionError:    
        msg = ('pdbfetcher requires the python package "%s", version %s or '
               ' later. You have version %s installed. You will need to upgrade.') % (package_name, minimum, v)

    if recommend_conda:
        install = ('\nTo install %s, we recommend the conda package manger. See http://conda.pydata.org for info on conda.\n'
                   'Using conda, you can install it with::\n\n    $ conda install %s') % (package_name, package_name)
        install += '\n\nAlternatively, with pip you can install the package with:\n\n    $ pip install %s' % package_name
    else:
        install = '\nWith pip you can install the package with:\n\n    $ pip install %s' % package_name
    
    if msg:
        banner = ('==' * 40)
        print('\n'.join([banner, banner, "", msg, install, "", banner, banner]))


# metadata for setup()
metadata = {
    'name': 'pdbfetcher',
    'version': VERSION,
    'author': __author__,
    'author_email': 'schwancr@stanford.edu',
    'license': 'GPL v3.0',
    'url': 'github.com/schwancr/pdbfetcher', 
    'download_url': 'github.com/schwancr/pdbfetcher',
    'platforms': ["Linux", "Mac OS X"],
    'description': DOCLINES[0],
    'long_description':"\n".join(DOCLINES[2:]),
    'packages': ['pdbfetcher', 'pdbfetcher.scripts'],
    'package_dir': {'pdbfetcher': 'pdbfetcher', 'pdbfetcher.scripts': 'scripts'},
    'zip_safe': False,
    'entry_points': {'console_scripts':
                ['get_pdb.py = pdbfetcher.scripts.get_pdb:entry_point']}
}



# Return the git revision as a string
# copied from numpy setup.py
def git_version():
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
        out = subprocess.Popen(cmd, stdout = subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = "Unknown"

    return GIT_REVISION


def write_version_py(filename='pdbfetcher/version.py'):
    cnt = """
# THIS FILE IS GENERATED FROM PDBFETCHER SETUP.PY
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
        GIT_REVISION = "Unknown"

    if not ISRELEASED:
        FULLVERSION += '.dev-' + GIT_REVISION[:7]

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'full_version' : FULLVERSION,
                       'git_revision' : GIT_REVISION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()

write_version_py()
setup(**metadata)

# running these after setup() ensures that they show
# at the bottom of the output, since setup() prints
# a lot to stdout. helps them not get lost
#warn_on_version('numpy', '1.6.0')
#warn_on_version('scipy', '0.11.0')
#warn_on_version('tables', '2.4.0', package_name='pytables')
#warn_on_version('fastcluster', '1.1.13')
#warn_on_version('yaml', package_name='pyyaml')
warn_on_version('mdtraj', '0.8.0')
