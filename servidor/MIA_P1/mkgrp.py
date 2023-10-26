import ctypes
import struct
from MIA_P1.utilities import *
from MIA_P1.load import *

class MK_GRP(ctypes.Structure):
    def __init__(self,listaParametros,salidaConsolaWeb) -> None:
        self.listaParametros = listaParametros
        self.salidaConsolaWeb = salidaConsolaWeb
        self.name="\0"
        
    def ejecutarGrupo(self):
        for val in self.listaParametros:
            if val.get("valoruser") != None:
                self.user = val.get("valoruser")
        