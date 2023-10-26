import ctypes
import struct
from MIA_P1.utilities import *
from MIA_P1.load import *
from MIA_P1.MBR import *


const = '3I c' #esta constante es para el mbr

class MKDISK(ctypes.Structure):
    __fields__ = [
        ('size', ctypes.c_int)
        #('path', ctypes.c_char * 50),
        #('fit', ctypes.c_char * 2 ),
        #('unit', ctypes.c_char * 1)
    ]
        
    def __init__(self,listaParametros,salidaConsolaWeb):
        self.listaParametros = listaParametros
        self.salidaConsolaWeb = salidaConsolaWeb
        self.size = 0
        self.path = '' #no se guarda
        self.fit = 'FF'
        self.unit = 'M' #no se guarda
    
    def ejecutar(self):
        for val in self.listaParametros:
            if val.get("valorfit") != None:
                self.fit = val.get("valorfit")
            elif val.get("valorunit") != None:
                self.unit = val.get("valorunit")
            elif val.get("valorsize") != None:
                self.size = int(val.get("valorsize"))
            elif val.get("rutaArchivo") != None:
                self.path = val.get("rutaArchivo") + val.get("nombrearchivo")
        #print(self.size, self.path, self.fit, self.unit)
        if self.path == "":
            #print("error, MKDISK path obligatorio")
            self.salidaConsolaWeb.append("error, MKDISK path obligatorio")
            return
        if self.size <= 0:
            #print("error, MKDISK size debe ser mayor a 0")
            self.salidaConsolaWeb.append("error, MKDISK size debe ser mayor a 0")
            return
        if self.fit != "BF" and self.fit != "FF" and self.fit != "WF":
            #print("error, MKDISK fit no se aceptan los valores")
            self.salidaConsolaWeb.append("error, MKDISK fit no se aceptan los valores")
            return
        if self.unit.lower() != "k" and self.unit.lower() != "m":
            #print("error, MKDISK unit no se aceptan los valores")
            self.salidaConsolaWeb.append("error, MKDISK unit no se aceptan los valores")
            return
        
        valorCreate = Fcreate_file(self.path)
        if not valorCreate:
            self.salidaConsolaWeb.append("Archivo creado exitosamente")
        else:
            self.salidaConsolaWeb.append("Error al crear archivo")
        Crrfile = open(self.path,"rb+")
        desplazamiento = 0
        self.calcularValoresSize()
        nuevoMBR = MBR(self.size,tiempo(),randomVal(1,100),convertirstringaBin(convertirValoresFit(self.fit,self.salidaConsolaWeb)))
        datos = nuevoMBR.doSerialize()
        Winit_size(Crrfile,self.size,self.salidaConsolaWeb )
        Fwrite_displacement(Crrfile,desplazamiento,datos) #archivo, desplazamiento y valores en binario
        Crrfile.close()
        
    
    
            
    def set_infomation(self, size, path, fit, unit):
        self.set_size(size)
        self.set_path(path)
        self.set_fit(fit)
        self.set_unit(unit)

    def display_info(self):
        self.salidaConsolaWeb.append(f"size: {self.size}")
        self.salidaConsolaWeb.append(f"path: {self.path.decode()}") # type: ignore
        self.salidaConsolaWeb.append(f"fit: {self.fit.decode()}") # type: ignore
        self.salidaConsolaWeb.append(f"unit: {self.unit.decode()}") # type: ignore
    

    def doSerialize(self): #esto es lo que escribire en el archivo binario
        objetoMk = struct.pack( #todo debe de estar en binario
            const,
            self.size,
            tiempo(),
            randomVal(1,100),
            convertirstringaBin(convertirValoresFit(self.fit))
        )
        return objetoMk

    def doDeserialize(self, data):
        sizeMK = struct.calcsize(const)
        datoBinarioMBR = data[:sizeMK]
        self.size, self.path, self.fit, self.unit = struct.unpack(const, datoBinarioMBR)
        
        
    def calcularValoresSize(self):
        if self.unit.lower() == "k":
            self.size = self.size * 1024
        elif self.unit.lower() == "m":
            self.size = self.size * 1024 * 1024
        
        