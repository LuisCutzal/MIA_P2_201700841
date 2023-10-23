import ctypes
import struct
from MIA_P1.utilities import *
from MIA_P1.load import *
from MIA_P1.MBR import *
from MIA_P1.EBR import *

class FDISK(ctypes.Structure):
    def __init__(self,listaParametros,salidaConsolaWeb):
        self.listaParametros = listaParametros
        self.salidaConsolaWeb = salidaConsolaWeb
        self.size = 0 #obligatorio
        self.path = '\0' #obligatorio
        self.name = '\0' #obligatorio
        self.unit = 'K' #kilobytes es default 
        self.type = 'P' #primaria es default 
        self.fit = 'WF'
        self.delete = '\0'
        self.add = 0
        self.constanteFDISK = 'I 6s i'
        self.temporalMBR = ""
    
    def ejecutarFDISK(self):
        if not self.agregarValores():
            #print("FDISK no se pudo ejecutar correctamente")
            self.salidaConsolaWeb.append("FDISK no se pudo ejecutar correctamente")
            return
        self.leerMBR()
        if self.temporalMBR == "":
            #print("Error, no se encuentra el MBR del archivo")
            self.salidaConsolaWeb.append("Error, no se encuentra el MBR del archivo")
            return
        listaParticiones = [self.temporalMBR.particion1,self.temporalMBR.particion2, self.temporalMBR.particion3, self.temporalMBR.particion4] # type: ignore
        if self.add == 0 and self.delete == '\0':
            if self.size <=0:
                #print(f"El valor de size no existe o es menor o igual a cero")
                self.salidaConsolaWeb.append(f"El valor de size no existe o es menor o igual a cero")
                return False
            #aca comienza todo lo que debe de hacer para agregar particiones sin usar add o delete en el comando
            if self.existeNombre(listaParticiones):
                #print("FDISK no se pudo ejecutar correctamente")
                self.salidaConsolaWeb.append("FDISK no se pudo ejecutar correctamente")
                return
            if self.type == "E":
                if self.comprobarExtendida(listaParticiones):
                    #print("FDISK no se pudo ejecutar correctamente")
                    #print("Error, Ya existe una extendida en el disco")
                    self.salidaConsolaWeb.append("FDISK no se pudo ejecutar correctamente")
                    self.salidaConsolaWeb.append("Error, Ya existe una extendida en el disco")
                    return
            if self.type == "L":
                if not self.comprobarExtendida(listaParticiones):
                    self.salidaConsolaWeb.append("FDISK no se pudo ejecutar correctamente")
                    self.salidaConsolaWeb.append("Error, no se puede agregar particion logica sin una extendida")
                    return
                else: 
                    self.escribirEBR()
                    return
            if not self.comprobarEspacio(listaParticiones):
                self.salidaConsolaWeb.append("FDISK no se pudo ejecutar correctamente")
                return
            if not self.comprobar4Particiones(listaParticiones):
                self.salidaConsolaWeb.append("Error FDISK, existen ya 4 particiones")
                return
            self.particionLibre(listaParticiones)
            self.temporalMBR.mbr_fecha_creacion = convertirTiempoEntero(self.temporalMBR.mbr_fecha_creacion)# type: ignore
            #self.temporalMBR.dsk_fit = convertirstringaBin(self.temporalMBR.dsk_fit)
            #print(self.temporalMBR.doSerialize())
            escribirArchivoExistente(self.path, 0, self.temporalMBR.doSerialize())# type: ignore

        if self.delete != '\0':
            #self.eliminarParticion(self.name)
            self.salidaConsolaWeb.append("Error el comando delete no existe")
            """if self.buscarnombre(listaParticiones,self.name):
                self.eliminarParticion(self.name)
            else:
                print("FDISK no se pudo ejecutar correctamente")
                print("El nombre de la particion no exite o ya fue eliminado")
                return"""
            
        if self.add > 0:
            self.salidaConsolaWeb.append("Error, el comando add no existe")
            #self.modificarEspacioParticion(self.name, self.add)
        if self.add <0:
            self.salidaConsolaWeb.append("Error, el comando add no existe")
            #self.modificarEspacioParticion(self.name, self.add)
    
    def agregarValores(self):
        for val in self.listaParametros:
            if val.get("valorsize") != None:
                self.size = int(val.get("valorsize"))
            elif val.get("rutaArchivo") != None:
                self.path = val.get("rutaArchivo") + val.get("nombrearchivo")
            elif val.get("valorname") != None:
                self.name = val.get("valorname")
            elif val.get("valorunit") != None:
                self.unit = val.get("valorunit")
            elif val.get("valortype") != None:
                self.type = val.get("valortype")
            elif val.get("valorfit") != None:
                self.fit = val.get("valorfit")
            elif val.get("valordelete") != None:
                self.delete = val.get("valordelete")
            elif val.get("valoradd") != None:
                self.add = val.get("valoradd")
        #print(self.listaParametros)
        
        if not archivoExistente(self.path):
            self.salidaConsolaWeb.append(f"No existe el archivo en la ruta {self.path}")
            return False
        
        self.calcularValoresSize()
        self.tipoDeParticion()
        self.fit = convertirValoresFit(self.fit)
        return True
    
    
    def calcularValoresSize(self):
        if self.unit.lower() == "b": #byes
            self.salidaConsolaWeb.append("particion en bytes")
        elif self.unit.lower() == "k": #kilobytes
            self.size = self.size * 1024
            self.salidaConsolaWeb.append("particion en kilobytes")
        elif self.unit.lower() == "m": #megabytes
            self.size = self.size * 1024 * 1024
            self.salidaConsolaWeb.append("particion en megabytes")
        else: self.salidaConsolaWeb.append(f"Error, el valor {self.unit} de unit no es valido")
    
    def tipoDeParticion(self):
        if self.type.lower() == "p":
            self.salidaConsolaWeb.append("particion primaria")
        elif self.type.lower() == "e":
            self.salidaConsolaWeb.append("particion extendida")
        elif self.type.lower() == "l":
            self.salidaConsolaWeb.append("particion logica")
        else: self.salidaConsolaWeb.append(f"Error, el valor {self.type} de type no es valido")
    
    
    def leerMBR(self):
        temporalMBR = MBR(0,0,0,0)
        datos = Fread_displacement(self.path,0,struct.calcsize(temporalMBR.constMBR) + struct.calcsize(temporalMBR.particion1.constanteParticion)*4, self.salidaConsolaWeb)
        temporalMBR.doDeserialize(datos) #ya tenemos los datos del mbr
        self.temporalMBR = temporalMBR
    
    def buscarnombre(self, listaparticiones, nombre):
        #esto es para particiones extendidas o primarias
        for particion in listaparticiones:
            if nombre in particion.part_name:
                return True
        return False
            

        
    def existeNombre(self, listaparticiones): #aca verificamos si el nombre de la particion existe
        for particion in listaparticiones:
            if particion.part_name == self.name:
                self.salidaConsolaWeb.append("El nombre de la particion ya existe")
                return True
        return False
    
    def particionLibre(self, listaparticiones): #aca vamos a escribir la particion en el archivo binario
        for particion in listaparticiones:
            if particion.part_status == "\x00":
                self.crearParticion(particion)
                return
            
    def crearParticion(self,particion):
        particion.part_status = "1"
        particion.part_type = self.type
        particion.part_fit = self.fit
        particion.part_start = self.comprobarStart([self.temporalMBR.particion1,self.temporalMBR.particion2, self.temporalMBR.particion3, self.temporalMBR.particion4])# type: ignore
        particion.part_s = self.size
        particion.part_name = self.name
        
        
    def comprobarEspacio(self, listaparticiones):
        cantidadEspacio = 0
        for particion in listaparticiones:
            if particion.part_status != "\x00":
                cantidadEspacio += particion.part_s
        if self.temporalMBR.mbr_tamano < cantidadEspacio + self.size: # type: ignore
            self.salidaConsolaWeb.append("No existe espacio suficiente para la particion que desea crear")
            return False
        return True
    
    def comprobar4Particiones(self, listaparticiones):
        for particion in listaparticiones:
            if particion.part_status == "\x00":
                return True
        return False
    
    def comprobarExtendida(self, listaparticiones):
        for particion in listaparticiones:
            if particion.part_type == "E":
                return True
        return False
    
    def comprobarStart(self, listaparticiones):
        partStart = struct.calcsize(self.temporalMBR.constMBR) + struct.calcsize(self.temporalMBR.particion1.constanteParticion)*4 # type: ignore
        for particion in listaparticiones:
            if particion.part_status != "\x00":
                partStart += particion.part_s
        return partStart
    
    def retornarExtendida(self, listaparticiones):
        for particion in listaparticiones:
            if particion.part_type == "E":
                return particion
    
    
    def escribirEBR(self):
        actualEBR = EBR()
        listaparticiones = [self.temporalMBR.particion1,self.temporalMBR.particion2, self.temporalMBR.particion3, self.temporalMBR.particion4] # type: ignore
        particionExtendida = self.retornarExtendida(listaparticiones)
        tam = struct.calcsize(actualEBR.constanteEBR)
        datosEBR = Fread_displacement(self.path,particionExtendida.part_start,tam) # type: ignore
        actualEBR.doDeserialize(datosEBR)
        actualizarSize = particionExtendida.part_s # type: ignore
        #comienza la lista enlazada
        if actualizarSize < self.size:
            self.salidaConsolaWeb.append("Error, no se puede crear la particion Logica")
            return        
        if actualEBR.part_s == 0: #es el primer ebr
            actualEBR.part_status = "1"
            actualEBR.part_fit = self.fit
            actualEBR.part_start = particionExtendida.part_start # type: ignore
            actualEBR.part_s = self.size
            actualEBR.part_next = actualEBR.part_next
            actualEBR.part_name = self.name
            escribirArchivoExistente(self.path, particionExtendida.part_start, actualEBR.doSerialize()) # type: ignore
            #print(particionExtendida.part_start)
            return
        while actualEBR.part_next != -1:
            actualEBR.doDeserialize(Fread_displacement(self.path, actualEBR.part_next, tam,self.salidaConsolaWeb))  #porque debemos de leer el siguiente
            actualizarSize -= actualEBR.part_s
            if actualEBR.part_name == self.name:
                self.salidaConsolaWeb.append("Ya existe la particion logica")
                return
            if actualizarSize < self.size:
                self.salidaConsolaWeb.append("No se puede crear particion ya que no existe espacio suficiente")
                return
                
        actualEBR.part_next = actualEBR.part_start + self.size
        escribirArchivoExistente(self.path,actualEBR.part_start,actualEBR.doSerialize())#solo su next
        nuevoEBR = EBR()
        nuevoEBR.part_status = "1"
        nuevoEBR.part_fit = self.fit
        nuevoEBR.part_start = actualEBR.part_next
        nuevoEBR.part_s = self.size
        nuevoEBR.part_next = -1
        nuevoEBR.part_name = self.name
        escribirArchivoExistente(self.path, nuevoEBR.part_start, nuevoEBR.doSerialize())
        

    def eliminarParticion(self, nombre):
        actualMBR = MBR(0,0,0,0)
        tam = struct.calcsize(actualMBR.constMBR) + struct.calcsize(actualMBR.particion1.constanteParticion)*4
        #leer el mbr
        datosMBR = Fread_displacement(self.path,0,tam,self.salidaConsolaWeb)
        #ahora deserealizar los datos
        actualMBR.doDeserialize(datosMBR)
        listaparticiones = [actualMBR.particion1, actualMBR.particion2, actualMBR.particion3, actualMBR.particion4]
        for i in range(len(listaparticiones)):
            #elimina particiones extendidas o primarias
            if listaparticiones[i].part_name == nombre:
                escribirArchivoExistente(self.path,listaparticiones[i].part_start, b'\0'* listaparticiones[i].part_s) #esto reescribe todo el tamaño de la particion rellena de 0
                #actualizamos el mbr
                listaparticiones[i].part_fit = '\0'
                listaparticiones[i].part_name = '\0' * 16
                listaparticiones[i].part_s = 0
                listaparticiones[i].part_start = 0
                listaparticiones[i].part_type = '\0'
                listaparticiones[i].part_status = '\0'
                actualMBR.mbr_fecha_creacion = convertirTiempoEntero(actualMBR.mbr_fecha_creacion)
                escribirArchivoExistente(self.path,0,actualMBR.doSerialize())
                return
        temporalParticion=""
        for particion in listaparticiones: #aca recorremos para obtener la particion extendida
            if particion.part_type == "E":
                #entra para bucar particiones logicas
                temporalParticion = particion
        if temporalParticion == "":
            return
        actualEBR = EBR()
        tamanioEBR = struct.calcsize(actualEBR.constanteEBR)
        datosEBR = Fread_displacement(self.path, temporalParticion.part_start, tamanioEBR,self.salidaConsolaWeb)
        actualEBR.doDeserialize(datosEBR)
        if actualEBR.part_name == nombre:
            if actualEBR.part_next != -1:
                siguiente = actualEBR.part_next
                actualEBR = EBR()
                actualEBR.part_next = siguiente
                escribirArchivoExistente(self.path,temporalParticion.part_start, actualEBR.doSerialize())
                self.salidaConsolaWeb.append(f"Particion logica {nombre} eliminada con exito")
                return
            #encontro la primera particion logica
            else:
                actualEBR = EBR()
                escribirArchivoExistente(self.path,temporalParticion.part_start,actualEBR.doSerialize())
                self.salidaConsolaWeb.append(f"Particion logica {nombre} eliminada con exito")
                return
        while actualEBR.part_next != -1:
            datosEBR = Fread_displacement(self.path, actualEBR.part_next, tamanioEBR,self.salidaConsolaWeb)
            siguienteEBR = EBR()
            siguienteEBR.doDeserialize(datosEBR)
            if siguienteEBR.part_name == nombre:
                escribirArchivoExistente(self.path, siguienteEBR.part_start, b'\0'* siguienteEBR.part_s)
                actualEBR.part_next = siguienteEBR.part_next
                siguienteEBR.part_status = "\0"
                siguienteEBR.part_fit = "\0"
                siguienteEBR.part_start = -1
                siguienteEBR.part_s = 0
                siguienteEBR.part_next = -1
                siguienteEBR.part_name = "\0" * 16
                escribirArchivoExistente(self.path, actualEBR.part_start, actualEBR.doSerialize())
                self.salidaConsolaWeb.append(f"Particion logica {nombre} eliminada con exito")
                return
            actualEBR = siguienteEBR
        self.salidaConsolaWeb.append(f"No se encontró la partición lógica {nombre}.")


                
                
    def modificarEspacioParticion(self, nombre_particion, espacio):
        # Buscar la partición con el nombre dado en el MBR
        listaParticiones = [self.temporalMBR.particion1, self.temporalMBR.particion2, self.temporalMBR.particion3, self.temporalMBR.particion4] # type: ignore
        particion = None
        for p in listaParticiones:
            if p.part_name == nombre_particion:
                particion = p
                break
        
        if particion is None:
            self.salidaConsolaWeb.append(f"No se encontró la partición {nombre_particion}.")
            return
        
        # Verificar si el espacio es negativo (quitar espacio) o positivo (agregar espacio)
        if espacio < 0:
            if abs(espacio) > particion.part_s:
                self.salidaConsolaWeb.append(f"No se puede quitar {abs(espacio)} espacio de la partición {nombre_particion}, espacio insuficiente.")
                return
            particion.part_s -= abs(espacio)
            self.salidaConsolaWeb.append(f"Se quitó {abs(espacio)} espacio de la partición {nombre_particion}.")
        elif espacio > 0:
            particion.part_s += espacio
            self.salidaConsolaWeb.append(f"Se agregó {espacio} espacio a la partición {nombre_particion}.")
        else:
            self.salidaConsolaWeb.append("No se realiza ninguna operación, el espacio es cero.")

        # Actualizar el MBR con los cambios en el tamaño de la partición
        self.temporalMBR.mbr_fecha_creacion = convertirTiempoEntero(self.temporalMBR.mbr_fecha_creacion) # type: ignore

        # Actualizar el tamaño de la partición en el MBR
        for i in range(len(listaParticiones)):
            if listaParticiones[i].part_name == nombre_particion:
                listaParticiones[i] = particion
                break

        # Escribir el MBR actualizado en el archivo
        mbr_data = bytearray(self.temporalMBR.doSerialize()) # type: ignore
        escribirArchivoExistente(self.path, 0, mbr_data)
