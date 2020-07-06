pyradamsa
==========================

`pyradamsa` provides an interface for calling libradamsa methods from within Python, allowing one to perform mutations on byte blocks (aka fuzzing). For more details see [radamsa](https://gitlab.com/akihe/radamsa) (a general-purpose fuzzer) and [libradamsa](https://github.com/andreafioraldi/libradamsa) (precompiled radamsa library).

## Usage

Install the package using `pip` (or [build](#building) it from source)
```bash
pip install pyradamsa
```

Do some fuzzing
```python
import pyradamsa

rad = pyradamsa.Radamsa()

mydata = b'GET /auth?pass=HelloWorld HTTP1.1'
fuzzed = rad.fuzz(mydata, seed=1337)
print(fuzzed)

> b'GET /auth?pass=HelloWorld HTTP\xc0\xb1.1'

# seed is randomly set if not provided
rad.fuzz(mydata)
> b'\tG\xf3\xa0\x81\x9c\xf7dLET \xe2\x81/aut\xf3\xa0\x80\xafHTTP2.rld HTTP2.rld HTTP3.2\xe1\xa0\x8e9'
rad.fuzz(mydata)
> b'GET /auth?pass=HelloWorld HTTP1.340282366920938463463374607431768211455'
etc.

# enforce static seed on initialization
rad = pyradamsa.Radamsa(seed=0)

# max_mut enforces a maximum length for returned data
# it defaults to (data length + an offset of 4096 bytes)
fuzzed = rad.fuzz(mydata, seed=1337, max_mut=10)
> b'GET /auth?'

# the offset may be overwritten on init
rad = pyradamsa.Radamsa(mut_offset=2048)
```

## Building
Currently wheels are available for linux i686 and x86_64
```sh
# Clone the repo
git clone --recurse-submodules https://github.com/tsundokul/pyradamsa.git
cd pyradamsa

# patch memory leak when reinitializing owl vm
patch libradamsa/libradamsa.c realloc.patch

# OPTIONAL: when using manylinux (https://github.com/pypa/manylinux)
docker run --rm -it -v `pwd`:/io quay.io/pypa/manylinux2010_x86_64 /bin/bash
cd /io && alias python='/opt/python/cp35-cp35m/bin/python3.5'
export PATH="/opt/python/cp35-cp35m/bin/:${PATH}"

# Install requirements
python -m pip install -r requirements.txt

# Build C extension (libradamsa.so)
python setup.py build_ext

# Run tests
./run_tests

# Build wheel
python setup.py bdist_wheel
```

## Contributing
* Fork the repo
* Check out a feature or bug branch
* Add your changes
* Update README when needed
* Submit a pull request to upstream repo
* Add description of your changes
* Ensure tests are passing
* Ensure branch is mergeable

_MIT License, 2020_ [@tim17d](https://twitter.com/tim17d)