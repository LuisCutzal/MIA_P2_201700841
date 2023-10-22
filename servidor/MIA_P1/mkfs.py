import ctypes
import struct
from MIA_P1.utilities import *
from MIA_P1.load import *

class MKFS(ctypes.Structure):
    def __init__(self, listaParametros):
        self.listaParametros = listaParametros
        self.id = '\0' #obligatorio
        self.type = '\0' #opcional

        
    def ejecutarMKFS(self):
        for val in self.listaParametros:
            if val.get("valorid") != None:
                self.id = val.get("valorid")
            elif val.get("valortype") != None:
                self.type = val.get("valortype")

        print(self.id)