import ctypes
import struct
from typing import Any
from MIA_P1.utilities import *
from MIA_P1.load import *

class bloqueArchivo(ctypes.Structure):
    def __init__(self):
        self.b_content = "\0"* 64 #char[ 64]
        self.constanteBloqueArchivo = '64s'
        
    def set_valores(self,content):
        self.b_content = content
    
    def doSerialize(self):
        objetoBloqueArchivo = struct.pack(
            self.constanteBloqueArchivo,
            convertirstringaBin(self.b_content)
        )
        return objetoBloqueArchivo
    
    def doDeserialize(self,dataBloqueArchivo):
        sizeContenido = struct.calcsize(self.constanteBloqueArchivo)
        datoBinario = dataBloqueArchivo[:sizeContenido]
        self.b_content = struct.unpack(self.constanteBloqueArchivo, datoBinario)
        self.b_content = deBinaString(self.b_content)
        return self
        