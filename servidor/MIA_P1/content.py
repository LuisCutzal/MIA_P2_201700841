import ctypes
import struct
from MIA_P1.utilities import *
from MIA_P1.load import *

class content(ctypes.Structure):
    def __init__(self):
        self.b_name = '\0' * 12
        self.b_inodo = -1
        self.constanteBloqueCarpeta = '12s i'
    
    def set_valores(self,bname, binodo):
        self.b_name = bname
        self.b_inodo = binodo
    
    def doSerialize(self):
        objetoContent = struct.pack(
            self.constanteBloqueCarpeta,
            convertirstringaBin(self.b_name),
            self.b_inodo
        )
        return objetoContent
    
    def doDeserialize(self, data):
        sizeContent = struct.calcsize(self.constanteBloqueCarpeta)
        datoBinario=data[:sizeContent]
        self.b_name, self.b_inodo = struct.unpack(self.constanteBloqueCarpeta, datoBinario)
        self.b_name=deBinaString(self.b_name)
        return self
        
    