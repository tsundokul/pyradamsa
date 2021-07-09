import ctypes
import pytest
import pyradamsa
import sys
import unittest

def test_lib_present():
    assert len(pyradamsa.Radamsa.lib_path()) > 0, 'library not found'

def test_lib_symbols():
    lib = ctypes.CDLL(pyradamsa.Radamsa.lib_path())
    assert hasattr(lib, 'radamsa_init')
    assert hasattr(lib, 'radamsa')
    assert hasattr(lib, 'radamsa_inplace')

def test_default_attrs():
    assert pyradamsa.Radamsa().mut_offset == 4096

    r = pyradamsa.Radamsa(17, 2048)
    assert r.seed == 17
    assert r.mut_offset == 2048

    r = pyradamsa.Radamsa(mut_offset=19)
    assert r.mut_offset == 19
    assert r.seed == None

@pytest.fixture
def data():
    return b'GET /auth?pass=HelloWorld HTTP1.1'

def test_seed_arg(data):
    assert pyradamsa.Radamsa().fuzz(
        data, seed=1338) == b'GET \xed\xaa\xad/auth?pas=Hello\xf3\xa0\x81\xb6World HTTP1.1'

def test_seed_wraparound(data):
    r = pyradamsa.Radamsa()
    assert r.fuzz(data, -1) == r.fuzz(data, sys.maxsize * 2 + 1)

def test_seed_static(data):
    r = pyradamsa.Radamsa(1337)
    assert r.fuzz(data) == r.fuzz(data)

def test_returned_len():
    data = b"\xaa\x00"*100
    assert len(pyradamsa.Radamsa(seed=1337).fuzz(data)) == 246