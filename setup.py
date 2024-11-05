#!/usr/bin/python3

import os
import platform
import subprocess
from setuptools import Extension, setup

from Cython.Build import cythonize

# -----------------------------------------------------------------------------
# constants

CWD = os.getcwd()

VERSION = '0.0.1'

PLATFORM = platform.system()

WITH_DYLIB = os.getenv("WITH_DYLIB", False)

LLAMACPP_INCLUDE = os.path.join(CWD, "thirdparty/llama.cpp/include")
LLAMACPP_LIBS_DIR = os.path.join(CWD, "thirdparty/llama.cpp/lib")

DEFINE_MACROS = []
EXTRA_COMPILE_ARGS = ['-std=c++14']
EXTRA_LINK_ARGS = []
EXTRA_OBJECTS = []
INCLUDE_DIRS = [
    "src/cyllama",
    LLAMACPP_INCLUDE,
]
LIBRARY_DIRS = [
    LLAMACPP_LIBS_DIR,
]
LIBRARIES = ["pthread"]


if WITH_DYLIB:
    EXTRA_OBJECTS.append(f'{LLAMACPP_LIBS_DIR}/libcommon.a')
    LIBRARIES.extend([
        'common',
        'ggml',
        'llama',
    ])
else:
    EXTRA_OBJECTS.extend([
        f'{LLAMACPP_LIBS_DIR}/libcommon.a', 
        f'{LLAMACPP_LIBS_DIR}/libllama.a', 
        f'{LLAMACPP_LIBS_DIR}/libggml.a',
    ])

INCLUDE_DIRS.append(os.path.join(CWD, 'include'))

if PLATFORM == 'Darwin':
    EXTRA_LINK_ARGS.append('-mmacosx-version-min=14.7')
    # add local rpath
    EXTRA_LINK_ARGS.append('-Wl,-rpath,' + LLAMACPP_LIBS_DIR)
    os.environ['LDFLAGS'] = ' '.join([
        '-framework Accelerate',
        '-framework Foundation',
        '-framework Metal',
        '-framework MetalKit',
    ])

if PLATFORM == 'Linux':
    EXTRA_LINK_ARGS.append('-fopenmp')


def mk_extension(name, sources, define_macros=None):
    return Extension(
        name=name,
        sources=sources,
        define_macros=define_macros if define_macros else [],
        include_dirs=INCLUDE_DIRS,
        libraries=LIBRARIES,
        library_dirs=LIBRARY_DIRS,
        extra_objects=EXTRA_OBJECTS,
        extra_compile_args=EXTRA_COMPILE_ARGS,
        extra_link_args=EXTRA_LINK_ARGS,
        language="c++",
    )


# ----------------------------------------------------------------------------
# COMMON SETUP CONFIG

common = {
    "name": "cyllama",
    "version": VERSION,
    "description": "A cython wrapper of the llama.cpp inference engine.",
    "python_requires": ">=3.8",
    # "include_package_data": True,
}


# forces cythonize in this case
subprocess.call("cythonize *.pyx", cwd="src/cyllama", shell=True)

if not os.path.exists('MANIFEST.in'):
    with open("MANIFEST.in", "w") as f:
        f.write("exclude src/cyllama/*.pxd\n")
        f.write("exclude src/cyllama/*.pyx\n")
        f.write("exclude src/cyllama/*.cpp\n")
        f.write("exclude src/cyllama/*.h\n")
        f.write("exclude src/cyllama/py.typed\n")

extensions = [
    mk_extension("cyllama.cyllama", sources=["src/cyllama/cyllama.pyx"]),
]

setup(
    **common,
    ext_modules=cythonize(
        extensions,
        compiler_directives = {
            'language_level' : '3',
            'embedsignature': False,     # default: False
            'emit_code_comments': False, # default: True
            'warn.unused': True,         # default: False
        },
    ),
    package_dir={"": "src"},
)

