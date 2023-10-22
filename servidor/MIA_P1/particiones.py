import ctypes
import struct
from MIA_P1.utilities import *
from MIA_P1.load import *

class PARTICION(ctypes.Structure):
   
    def __init__(self):
        self.part_status = '\0'
        self.part_type = '\0'
        self.part_fit = '\0'
        self.part_start = 0
        self.part_s = 0
        self.part_name = '\0' * 16
        self.constanteParticion = '3c 2I 16s'
    
    def set_valores(self,part_status,part_type,part_fit,part_start,part_s,part_name):
        self.part_status = part_status
        self.part_type = part_type
        self.part_fit = part_fit
        self.part_start = part_start
        self.part_s = part_s
        self.part_name = part_name
    
    def doSerialize(self):#esto es lo que escribire en el archivo binario
        nuevaParticion = struct.pack(
            self.constanteParticion,
            convertirstringaBin(self.part_status),
            convertirstringaBin(self.part_type),
            convertirstringaBin(self.part_fit),
            self.part_start,
            self.part_s,
            convertirstringaBin(self.part_name)
        )
        return nuevaParticion
    
    def doDeserialize(self, data):
        partSize = struct.calcsize(self.constanteParticion)
        datosParticion = struct.unpack(self.constanteParticion, data)
        if datosParticion[3] == 0 and datosParticion[4] == 0:
            return self
        self.part_status = deBinaString(datosParticion[0]) #convertimos los datos binarios a strings
        self.part_type= deBinaString(datosParticion[1]) #convertimos los datos binarios a strings
        self.part_fit= deBinaString(datosParticion[2]) #convertimos los datos binarios a strings
        self.part_start= datosParticion[3]
        self.part_s = datosParticion[4]
        self.part_name = deBinaString(datosParticion[5])
        return self