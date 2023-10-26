import ctypes
import struct
from typing import Any
from MIA_P1.utilities import *
from MIA_P1.load import *

class bloqueArchivo(ctypes.Structure):
    def __init__(self,listaParametros, SalidaConsolaWeb):
        self.listaParametros= listaParametros
        self.SalidaConsolaWeb = SalidaConsolaWeb
        self.b_content = "\0"* 64 #char[ 64]
        self.constanteBloqueArchivo = '64s'
        