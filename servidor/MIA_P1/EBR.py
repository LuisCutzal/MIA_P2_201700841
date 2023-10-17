import ctypes
import struct
from utilities import *
from load import *
class EBR(ctypes.Structure): #es un EBR porque tendre muchos objetos ebr
    
    def __init__(self):
        self.part_status = "\0"
        self.part_fit = "\0"
        self.part_start = 0
        self.part_s = 0
        self.part_next = -1
        self.part_name = "\0" * 16
        self.constanteEBR = '2c 2I i 16s' # 2 char, 2 enteros sin signo, 1 entero con signo y una cadena de chars
        
    
    def set_valores(self, part_status, part_fit, part_start,part_s, part_next, part_name ):
        self.part_status = part_status
        self.part_fit = part_fit
        self.part_start = part_start
        self.part_s = part_s
        self.part_next = part_next
        self.part_name = part_name
    
    
    def doSerialize(self): #esto es lo que escribire en el archivo binario
        nuevaExtendida = struct.pack(
            self.constanteEBR,
            convertirstringaBin(self.part_status),
            convertirstringaBin(self.part_fit),
            self.part_start,
            self.part_s,
            self.part_next,
            convertirstringaBin(self.part_name)
        ) 
        return nuevaExtendida
    
    def doDeserialize(self, data):
        partSize = struct.calcsize(self.constanteEBR)
        datosEBR = struct.unpack(self.constanteEBR,data)
        if datosEBR[2] == 0 and datosEBR[3] == 0:
            return self
        self.part_status = deBinaString(datosEBR[0])
        self.part_fit = deBinaString(datosEBR[1])
        self.part_start = (datosEBR[2])
        self.part_s = (datosEBR[3])
        self.part_next = (datosEBR[4])
        self.part_name = deBinaString(datosEBR[5])
        return self    