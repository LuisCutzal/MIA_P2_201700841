import ctypes
import struct
from MIA_P1.utilities import *
from MIA_P1.load import *

class SuperBloque(ctypes.Structure):
    def __init__(self):
        self.s_filesystem_type=0
        self.s_inodes_count =0
        self.s_blocks_count=0
        self.s_free_blocks_count =0
        self.s_free_inodes_count =0
        self.s_mtime = 0 #tiempo
        self.s_umtime =0 #tiempo
        self.s_mnt_count = 0
        self.s_magic =0
        self.s_inode_s=0
        self.s_block_s=0
        self.s_firts_ino=0
        self.s_first_blo=0
        self.s_bm_inode_start=0
        self.s_bm_block_start=0
        self.s_inode_start=0
        self.s_block_start=0
        self.constanteSuperBloque = '17I'
        
        
        
        
        """
        def calculate_value_of_n(self, size_partition, super_block, inode, content):
        n = (size_partition - struct.calcsize(super_block.FORMATSUPERBLOCK)) / (4 + struct.calcsize(inode.FORMARTINODETABLE) + 3 * struct.calcsize(content.FORMARTCONTENT)*4)
        return math.floor(n)
        """
        
        """ 
        class Bitmap:
            def __init__(self)->None:
                self._FORMATBITMAPINODE = "c"
                self.size_bitmap = 0
                self.array_bitmap = []
        def serialize_bitmap(self, array_bitmap, size_bitmap):
                if len(array_bitmap) == 0:
                    self.size_bitmap = size_bitmap
                    self._FORMATBITMAPINODE = str(self.size_bitmap) + self._FORMATBITMAPINODE
                    self.array_bitmap = [b'0'] * self.size_bitmap
                else:
        self.size_bitmap = len(array_bitmap)
                    self.array_bitmap = [fn([]).string_to_bytes(item) for item in array_bitmap]
                    self._FORMATBITMAPINODE = str(len(self.array_bitmap)) + self._FORMATBITMAPINODE    
                fns = fn([])
        return fns.serialize(self._FORMATBITMAPINODE, *self.array_bitmap)
        
            def deserialize_bitmap(self, data, size_bitmap):
            if len(data) != size_bitmap:
                print("Error al deserializar bitmap de inodos no coincide con el tamaño")
                return None
    self.size_bitmap = size_bitmap
            self._FORMATBITMAPINODE = str(self.size_bitmap) + self._FORMATBITMAPINODE
            data = fn([]).deserialize(self._FORMATBITMAPINODE, data)
    if data is None:
                print("Error al deserializar bitmap de inodos")
                return None
            self.array_bitmap = [fn([]).bytes_to_string(item) for item in data]
            return self
        """