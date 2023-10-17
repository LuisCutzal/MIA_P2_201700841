import ctypes
import struct
from utilities import *
from load import *

class MKFS(ctypes.Structure):
    def __init__(self, listaParametros):
        self.listaParametros = listaParametros
        self.id = '\0' #obligatorio
        self.type = '\0' #opcional
        self.fs = 'ext2' #opcional
        self.constanteMKFS = '3c'
        
    def ejecutarMKFS(self):
        for val in self.listaParametros:
            if val.get("valorid") != None:
                self.id = val.get("valorid")
            elif val.get("valortype") != None:
                self.type = val.get("valortype")
            elif val.get("valorfs") != None:
                self.fs = val.get("valorfs")
        print(self.fs)