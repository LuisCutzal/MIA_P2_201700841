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
        
    def doSerialize(self):
        objetoSuperBloque = struct.pack(
            self.constanteSuperBloque,
            self.s_filesystem_type,
            self.s_inodes_count,
            self.s_blocks_count,
            self.s_free_blocks_count,
            self.s_free_inodes_count,
            self.s_mtime,
            self.s_umtime,
            self.s_mnt_count,
            self.s_magic,
            self.s_inode_s,
            self.s_block_s,
            self.s_firts_ino,
            self.s_first_blo,
            self.s_bm_inode_start,
            self.s_bm_block_start,
            self.s_inode_start,
            self.s_block_start            
        )
        return objetoSuperBloque
    
    def doDeserialize(self, data):
        sizeContent = struct.calcsize(self.constanteSuperBloque)
        datoBinario = data[:sizeContent]
        self.s_filesystem_type,self.s_inodes_count,self.s_blocks_count,self.s_free_blocks_count,self.s_free_inodes_count,self.s_mtime,self.s_umtime,self.s_mnt_count,self.s_magic,self.s_inode_s,self.s_block_s,self.s_firts_ino,self.s_first_blo,self.s_bm_inode_start,self.s_bm_block_start,self.s_inode_start,self.s_block_start = struct.unpack(self.constanteSuperBloque,datoBinario)
        return self
        
        
        
        
        
        """
        superbloque -> superbloque
        bitmap inodos -> array
        bitmapbloques -> array
        inodos -> tablaInodos
        bloques -> bloquearchivo, bloquecarpeta
        """