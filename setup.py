from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import glob
import setuptools

__version__ = '0.0.3'


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

def get_libsodium_path(libsodiumver='libsodium.so.23'):
    '''
    Function to find the path to the requisite libsodium library.

    Version can be specified as desired, defaults to 23 (e.g. - looks for libsodium.so.23)
    '''
    paths = glob.glob('/usr/lib/**/{:s}'.format(libsodiumver), recursive=True)
    if len(paths) == 0:
        print("ERROR: Please install libsodium == {:s}".format(libsodiumver))
        sys.exit(1)
    else:
        return paths[0]


ext_modules = [
    Extension(
        'verushash',
        ['src/compat/glibc_compat.cpp',
         'src/compat/glibc_sanity.cpp',
         'src/compat/glibcxx_sanity.cpp',
         'src/compat/strnlen.cpp',
         'src/crypto/haraka.c',
         'src/crypto/haraka_portable.c',
         'src/crypto/ripemd160.cpp',
         'src/crypto/sha256.cpp',
         'src/crypto/uint256.cpp',
         'src/crypto/utilstrencodings.cpp',
         'src/crypto/verus_hash.cpp',
         'src/crypto/verus_clhash.cpp',
         'src/crypto/verus_clhash_portable.cpp',
         'src/support/cleanse.cpp',
         'src/blockhash.cpp',
         'src/main.cpp'],
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True)
        ],
        extra_objects=[
            get_libsodium_path()
        ],
        language='c++'
    ),
]


# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14/17] compiler flag.

    The newer version is prefered over c++11 (when it is available).
    """
    flags = ['-std=c++17', '-std=c++14', '-std=c++11']

    for flag in flags:
        if has_flag(compiler, flag): return flag

    raise RuntimeError('Unsupported compiler -- at least C++11 support '
                       'is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': ['-Wl,--whole-archive',
                 '-fPIC',
                 '-fexceptions',
                 '-Ofast',
                 '-march=native',
                 '-Wno-reorder',
                 '-g'],
    }
    l_opts = {
        'msvc': [],
        'unix': [],
    }

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc++', '-mmacosx-version-min=10.7']
        c_opts['unix'] += darwin_opts
        l_opts['unix'] += darwin_opts

    def build_extensions(self):
        if '-Wstrict-prototypes' in self.compiler.compiler_so:
            self.compiler.compiler_so.remove('-Wstrict-prototypes')
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts
        build_ext.build_extensions(self)

setup(
    name='verushash',
    version=__version__,
    author='Michael Toutonghi',
    author_email='',
    url='https://github.com/miketout/verushashpy',
    description='Native Verus Hash module for Python',
    long_description='A Verus Hash module supporting VerusHash 1.0 - 2.2, written in C++',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.4'],
    setup_requires=['pybind11>=2.4'],
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)


static_libraries = ['igraph']
static_lib_dir = '/system/lib'
libraries = ['z', 'xml2', 'gmp']
library_dirs = ['/system/lib', '/system/lib64']

if sys.platform == 'win32':
    libraries.extend(static_libraries)
    library_dirs.append(static_lib_dir)
    extra_objects = []
else: # POSIX
    extra_objects = ['{}/lib{}.a'.format(static_lib_dir, l) for l in static_libraries]

