import ctypes
from MIA_P1.utilities import *
from MIA_P1.load import *
from MIA_P1.content import *
class bloqueCarpeta(ctypes.Structure):
    def __init__(self):
        self.b_content = [content(),content(),content(),content()]#array content[4]
    
    def set_valores(self, nuevo):
        self.b_content = nuevo
    
    def doSerialize(self):
        contenidoData = b''
        for contenido in self.b_content:
            contenidoData += contenido.doSerialize()
        return contenidoData

    def doDeserialize(self,datosContenido):
        if len(datosContenido) != 64:
            print("Error, el contenido no es igual a 64")
            return self
        temporalContenido = content()
        for i in range(4):
            self.b_content[i].doDeserialize(datosContenido[i * struct.calcsize(temporalContenido.constanteBloqueCarpeta): (i+1) * struct.calcsize(temporalContenido.constanteBloqueCarpeta)])
        return self