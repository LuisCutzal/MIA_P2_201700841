import ctypes
import struct
from MIA_P1.utilities import *
from MIA_P1.load import *

class UNMOUNT(ctypes.Structure):
    def __init__(self, listaides,salidaConsolaWeb):
        self.listaides = listaides
        self.salidaConsolaWeb = salidaConsolaWeb
        self.id = '\0'
        self.constanteUNMOUNT = 'C'
    
    def ejecutarUNMOUNT(self, listaMount):
        for val in self.listaides:
            if val.get("valorid") != None:
                self.id = val.get("valorid")
        for identificadores in listaMount:
            if identificadores['id'] == self.id:
                listaMount.remove(identificadores)
                self.salidaConsolaWeb.append(f"Se desmonto {self.id} correctamente")
                return
        self.salidaConsolaWeb.append(f"No se encontro el {self.id} ya sea que no existe o ya esta desmontado")
            
                
    
    
    