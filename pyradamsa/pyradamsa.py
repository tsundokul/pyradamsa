
from ctypes import *
from glob import glob
from os import path
from random import randint
from sys import maxsize

class Radamsa():

    def __init__(self, seed=None, mut_offset=4096):
        self.seed = seed
        self.mut_offset = mut_offset

        # Load shared library
        self.LIB = CDLL(self.lib_path())

        # Set word size and max value for seeds
        self.MAX_WORD = maxsize * 2 + 1
        _is_64 = self.MAX_WORD.bit_length() // 64
        self.C_WORD = c_uint64 if _is_64 else c_uint32

        # Declare ctypes interfaces for functions
        self._declare_sigs()


    def _declare_sigs(self):
        """C signatures for libradamsa functions
        extern void init()
        extern size_t radamsa(uint8_t * ptr, size_t len, uint8_t * target,
            size_t max, unsigned int seed)
        extern size_t radamsa_inplace(uint8_t * ptr, size_t len,
            size_t max, unsigned int seed)"""
        self.LIB.init.argtypes = []
        self.LIB.init.restype = None

        self.LIB.radamsa.restype = c_size_t
        self.LIB.radamsa.argtypes = [POINTER(c_uint8), c_size_t,
                                    POINTER(c_uint8), c_size_t, self.C_WORD]

        self.LIB.radamsa_inplace.restype = c_size_t
        self.LIB.radamsa_inplace.argtypes = [
            POINTER(c_uint8), c_size_t, c_size_t, self.C_WORD]

    def fuzz(self, data, seed=None, max_mut=None):
        # (re) initialize OWL/Scheme VM to ensure output repeatability,
        # otherwise the VM's heap will get corrupted
        self.LIB.init()

        if seed is None:
            if self.seed is None:
                seed = randint(0, self.MAX_WORD)
            else:
                seed = self.seed

        seed = self.C_WORD(seed & self.MAX_WORD)
        data_len = len(data)
        data_to_mutate = (c_uint8 * data_len)(*data)
        
        length = c_size_t(data_len)
        _max_mut = max_mut or data_len + self.mut_offset
        max_mut = c_size_t(_max_mut)
        
        # Adjust destination buffer in regard to max_mut
        buffer = (c_uint8 * _max_mut)()

        block_size = int(self.LIB.radamsa(
            data_to_mutate,
            length,
            buffer,
            max_mut,
            seed
            )
        )
        return bytes(buffer[:block_size])

    @staticmethod
    def lib_path():
        mod_dir = path.dirname(path.realpath(__file__))
        lib_dir = path.join(mod_dir, 'lib', 'libradamsa*')
        so_list = glob(lib_dir)

        if len(so_list) != 1:
            raise Exception('No shared library found in module tree')

        return so_list[0]
