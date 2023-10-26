import os
from MIA_P1.load import *
class RMDISK():
    def __init__(self,salidaConsolaWeb):
        self.salidaConsolaWeb = salidaConsolaWeb
    
    def ejecutarRMDISK(self,diccionarioRuta):
        ruta = diccionarioRuta['rutaArchivo'] + diccionarioRuta['nombrearchivo']
        #print(ruta)
        if archivoExistente(ruta):
            os.remove(ruta)
            self.salidaConsolaWeb.append(f"El archivo {diccionarioRuta['nombrearchivo']} fue eliminado")
        else: self.salidaConsolaWeb.append("El archivo no existe")
        