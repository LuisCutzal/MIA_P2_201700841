import ctypes
import struct
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
        self.i_block= [-1] * 15
        self.i_type="\0"
        self.i_perm=0
        self.constanteTablaInodos = '6I 15i c I'
    
    def set_values(self, uid,gid,s,atime,ctime,mtime,block,type,perm):
        self.i_uid=uid
        self.I_gid=gid
        self.i_s=s
        self.i_atime=atime
        self.i_ctime=ctime
        self.i_mtime=mtime 
        self.i_block=block
        self.i_type=type
        self.i_perm=perm
    
    
    def doSerialize(self):
        objetoTabla = struct.pack(
            self.constanteTablaInodos,
            self.i_uid,
            self.I_gid,
            self.i_s,
            self.i_atime,
            self.i_ctime,
            self.i_mtime,
            *self.i_block,
            convertirstringaBin(self.i_type),
            self.i_perm
        )
        return objetoTabla
    
    def doDeserialize(self, dataTabla):
        sizeContent = struct.calcsize(self.constanteTablaInodos)
        datoBinario = dataTabla[:sizeContent]
        self.i_uid,self.I_gid,self.i_s,self.i_atime,self.i_ctime,self.i_mtime,*self.i_blockl,self.i_type,self.i_perm= struct.unpack(self.constanteTablaInodos,datoBinario)
        self.i_type= deBinaString(self.i_type)
        return self