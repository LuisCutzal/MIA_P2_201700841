import ctypes
import struct
from MIA_P1.utilities import *
from MIA_P1.load import *
#este archivo contiene el bitmap de inodos y el bitmap de bloques
#todo este bitmap es "n"
class bitMap(ctypes.Structure):
    def __init__(self):
        self.tamBitMap =0
        self.contenidoBitMap =[]
        self.constanteBitMap = 'c'
    
    def set_values(self, tambit, contenbit):
        self.tamBitMap =tambit
        self.contenidoBitMap =contenbit
    
    def doSerialize(self):
        if len(self.contenidoBitMap) == 0:
            self.constanteBitMap = str(self.tamBitMap) + self.constanteBitMap
            self.contenidoBitMap = [b'0']* self.tamBitMap
        else:
            self.tamBitMap = len(self.contenidoBitMap)
            self.contenidoBitMap = [convertirstringaBin(item) for item in self.contenidoBitMap]
            self.constanteBitMap = str(len(self.contenidoBitMap)) + self.constanteBitMap
        objetoBitMap=struct.pack(
            self.constanteBitMap,
            *self.contenidoBitMap
        ) 
        return objetoBitMap
    
    def doDeserialize(self, dataBitMap, tam):
        if len(dataBitMap) != tam:
            print("Error, el tamaño del bitmap no es el correcto")
            return None
        self.tamBitMap = tam
        self.constanteBitMap = str((self.tamBitMap)) + self.constanteBitMap
        dataBitMap = struct.unpack(self.constanteBitMap, dataBitMap)
        self.contenidoBitMap = [deBinaString(item) for item in dataBitMap]
        return self