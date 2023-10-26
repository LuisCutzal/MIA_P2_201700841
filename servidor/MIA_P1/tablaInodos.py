import ctypes
import struct
from typing import Any
from MIA_P1.utilities import *
from MIA_P1.load import *

class TablaInodos(ctypes.Structure):
    def __init__(self):
        self.i_uid=0
        self.I_gid=0
        self.i_s=0
        self.i_atime=0 #tiempo
        self.i_ctime=0#tiempo
        self.i_mtime=0 #tiempo
        self.i_block=0
        self.i_type="\0"
        self.i_perm=0
        self.constanteTablaInodos = '7I s I'