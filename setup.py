#!/usr/bin/env python3
import sys
from setuptools import setup, Extension

extra_link_args = []
if sys.platform == 'linux':
    extra_link_args.append('-lrt')

libradamsa = Extension(
    "libradamsa",
    sources=["libradamsa/libradamsa.c"],
    include_dirs=["libradamsa"],
    py_limited_api=True,
    extra_compile_args=["-O3"],
    extra_link_args=extra_link_args,
)

setup(
    ext_modules=[libradamsa],
    options={
        'build_ext': {'build_lib': 'pyradamsa/lib'}
    }
)
