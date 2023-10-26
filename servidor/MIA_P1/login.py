import ctypes
import struct
from MIA_P1.utilities import *
from MIA_P1.load import *

class LoginFront(ctypes.Structure):
    def __init__(self,listaParametros,salidaConsolaWeb) -> None:
        self.listaParametros = listaParametros
        self.salidaConsolaWeb = salidaConsolaWeb
        self.user="\0"
        self.password ="\0"
        self.id="\0"
        
    def ejecutarLoginFront(self):
        for val in self.listaParametros:
            if val.get("valoruser") != None:
                self.user = val.get("valoruser")
            elif val.get("valorpassword") != None:
                self.password = val.get("valorpassword")
            elif val.get("valorid") != None:
                self.id = val.get("valorid")