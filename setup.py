
from setuptools import setup, Extension, find_packages
from pyradamsa.version import __version__

libradamsa = Extension('libradamsa',
   sources=['radamsa/c/libradamsa.c'],
   include_dirs=['radamsa/c'],
   py_limited_api=True,
   extra_compile_args=['-O3', '-lrt']
)

setup(name='pyradamsa',
      version=__version__,
      description='Python bindings for radamsa fuzzing library.',
      long_description_content_type='text/markdown',
      long_description=open('README.md').read().strip(),
      author='Daniel Timofte @tim17d',
      author_email='timofte.daniel@tuta.io',
      url='https://github.com/tsundokul/pyradamsa',
      py_modules=['pyradamsa'],
      install_requires=[],
      license='MIT License',
      zip_safe=False,
      keywords='radamsa fuzzing libradamsa',
      packages=['pyradamsa'],
      include_package_data=True,
      setup_requires=["wheel"],
      classifiers=[
         "Development Status :: 4 - Beta",
         "Topic :: Security",
         "Operating System :: POSIX :: Linux",
         "License :: OSI Approved :: MIT License",
         'Programming Language :: Python :: 3',
      ],
      ext_modules=[libradamsa],
      options={
          'bdist_wheel': {'python_tag': 'cp30', 'py_limited_api': 'cp32'},
          'build_ext': {'build_lib': 'pyradamsa/lib'}
      }
   )
