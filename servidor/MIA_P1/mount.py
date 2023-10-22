import ctypes
import struct
from MIA_P1.utilities import *
from MIA_P1.load import *
from MIA_P1.MBR import *
from MIA_P1.EBR import *
class MOUNT(ctypes.Structure):
    def __init__(self, listaParametros):
        self.listaParametros = listaParametros
        self.path = '\0' #obligatorio
        self.name = '\0' #obligatorio
        self.nombrearchivo = ""
        self.constanteMOUNT = '2c'
        self.temporalMBR = ""
        self.temportalEBR = ""
        
    def ejecutarMOUNT(self, listaMount):
        if not self.validarMount():
            print("Error, no se pudo ejecutar el comando mount")
            return
        if self.contieneValores(listaMount):
            return      
        self.leerMBR()
        if self.temporalMBR == "":
            print("Error, no se encuentra el MBR del archivo")
            return
        if not self.buscarParticion(listaMount):
            print(f"No se encontro la particion {self.name}")
            return
        
    def contieneValores(self, listaMount):
        if listaMount:
            return True
        else: return False
   
    def validarMount(self):
        for val in self.listaParametros:
            if val.get("rutaArchivo") != None:
                self.path = val.get("rutaArchivo") + val.get("nombrearchivo")
                self.nombrearchivo = val.get("nombrearchivo")
            elif val.get("valorname") != None:
                self.name = val.get("valorname")
        if not archivoExistente(self.path):
            print(f"No existe el archivo en la ruta {self.path}")
            return
        return True
    
    def leerMBR(self):
        temporalMBR = MBR(0,0,0,0)
        datos = Fread_displacement(self.path,0,struct.calcsize(temporalMBR.constMBR) + struct.calcsize(temporalMBR.particion1.constanteParticion)*4)
        temporalMBR.doDeserialize(datos) #ya tenemos los datos del mbr
        self.temporalMBR = temporalMBR
    
    def retornarExtendida(self, listaparticiones):
        for particion in listaparticiones:
            if particion.part_type == "E":
                return particion
    
    def montarLogica(self, listaparticiones, listaMount, contador):
        #aca se coloca la parte del nombre de la particion
        actualEBR = EBR()
        particionExtendida = self.retornarExtendida(listaparticiones)
        tam = struct.calcsize(actualEBR.constanteEBR)
        datosEBR = Fread_displacement(self.path,particionExtendida.part_start,tam)
        actualEBR.doDeserialize(datosEBR)
        self.temportalEBR = actualEBR
        if actualEBR.part_name == self.name: #primera particion
            contador +=1
            datosMount = {
                "path":self.path,
                "id": self.generarIdParticion(contador),
                "particion": actualEBR
            }
            listaMount.append(datosMount)
            print(f"Se monto la particion {self.name} con identificador {datosMount['id']}")
            return True
        contador +=1    
        while actualEBR.part_next != -1:
            actualEBR.doDeserialize(Fread_displacement(self.path, actualEBR.part_next, tam))
            contador +=1
            if actualEBR.part_name == self.name:
                datosMount = {
                    "path":self.path,
                    "id": self.generarIdParticion(contador),
                    "particion": actualEBR
                }
                listaMount.append(datosMount)
                print(f"Se monto la particion {self.name} con identificador {datosMount['id']}")
                return True
        return False

    def generarIdParticion(self, numParticion,):
        nombre = self.nombrearchivo.split(".")
        return "41"+str(numParticion)+nombre[0]
        
    def buscarParticion(self,listaMount):
        listaParticiones = [self.temporalMBR.particion1,self.temporalMBR.particion2, self.temporalMBR.particion3, self.temporalMBR.particion4]
        contadorparticion = 0
        for particion in listaParticiones: #para particiones primarias
            if particion.part_name == self.name:
                datosMount = {
                    "path":self.path,
                    "id": self.generarIdParticion(contadorparticion),
                    "particion": particion
                }
                listaMount.append(datosMount)
                print(f"Se monto la particion {self.name} con identificador {datosMount['id']}")
                return True
            contadorparticion +=1
        #comienza particiones logicas
        return self.montarLogica(listaParticiones,listaMount,contadorparticion)
    
"""
ultimos digitos carnet + numero particion + nombredisco
para los ids -> 411disco1
"""