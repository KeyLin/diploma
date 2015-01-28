#@+leo-ver=4
#@+node:@file setup.py
import sys

from distutils.core import setup, Extension
from Pyrex.Distutils import build_ext

incDirs = ['../libspeex', '/usr/include/speex', '/usr/local/include/speex']
libs = []
libDirs = []
runtimeLibDirs = []
cMacros = []
#extraLinkArgs = ['-g', '/usr/lib/libspeex.a'] # static
extraLinkArgs = ['-g', '-lspeex'] # shared

if sys.platform == 'win32':
    libDirs.append('..\\win32\\Release')
    libs = []
    extraLinkArgs = ['..\\win32\\libspeex\\Release\\libspeex.lib']

speexmodule = Extension('speex',
                        ['speex.pyx'],
                        define_macros=cMacros,
                        include_dirs=incDirs,
                        libraries=libs,
                        library_dirs=libDirs,
                        runtime_library_dirs=runtimeLibDirs,
                        extra_compile_args=['-g'],
                        extra_link_args=extraLinkArgs
                        )

setup(name = 'speex',
      version = '1.0',
      description = 'Python interface to the Speex audio codec',
      ext_modules = [speexmodule],
      cmdclass = {'build_ext': build_ext},
      )
#@-node:@file setup.py
#@-leo
