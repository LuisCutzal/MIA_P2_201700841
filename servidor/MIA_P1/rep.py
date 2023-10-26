from MIA_P1.MBR import *
from MIA_P1.EBR import *
from MIA_P1.load import *
import struct
import graphviz
import shutil
class REP():
    def __init__(self, listaparametros,salidaConsolaWeb):
        self.listaparametros = listaparametros
        self.salidaConsolaWeb = salidaConsolaWeb
        self.identificador = "" #Indica el id de la partición que se utilizará
        self. path =""
        self.name = "" #Nombre del reporte a generar. 
        self.ruta = ""
        self.temporalMBR = ""
        self.nombreArchivo =""
        
    def ejecutarRep(self, listaMount):
        if not self.agregarvalores():
            self.salidaConsolaWeb.append("El comandno rep no se pudo ejecutar correctamente")
            return
        if not self.verificarNombre():
            self.salidaConsolaWeb.append("El nombre que ingreso en el comando REP no es valido")
            return
        if self.name == "mbr":
            self.crearGrafoMBR(listaMount)
            return
        if self.name == "disk":
            self.crearGrafoDisk(listaMount)
            return
        
        
    def agregarvalores(self):
        for val in self.listaparametros:
            if val.get("valorid") is not None:
                self.identificador = val.get("valorid")
            elif val.get("rutaArchivo") is not None:
                self.path = val.get("rutaArchivo") + val.get("nombrearchivo")
                self.nombreArchivo = val.get("nombrearchivo")
            elif val.get("valorname") is not None:
                self.name = val.get("valorname")
            elif val.get("ruta") is not None:
                self.ruta = val.get("ruta") + val.get("nombre")
        return True
    def verificarNombre(self):
        if self.name == "mbr":
            self.salidaConsolaWeb.append("Generar reporte MBR")
            return True
        elif self.name == "disk":
            self.salidaConsolaWeb.append("Generar reporte DISK")
            return True
        elif self.name == "bm_inode":
            self.salidaConsolaWeb.append("Generar reporte bm_inode")
            return True
        elif self.name == "bm_block":
            self.salidaConsolaWeb.append("Generar reporte bm_block")
            return True
        elif self.name == "tree":
            self.salidaConsolaWeb.append("Generar reporte tree")
            return True
        elif self.name == "sb":
            self.salidaConsolaWeb.append("Generar reporte sb")
            return True
        elif self.name == "file":
            self.salidaConsolaWeb.append("Generar reporte file")
            return True
        else: return      
    
    
    def crearGrafoMBR(self,listaMount):
        direccion=""
        for identificadores in listaMount:
            if identificadores['id'] == self.identificador:
                direccion= identificadores['path']
                particion = identificadores['particion']
                temporalMBR = MBR(0,0,0,0)
                datos = Fread_displacement(direccion,0,struct.calcsize(temporalMBR.constMBR) + struct.calcsize(temporalMBR.particion1.constanteParticion)*4,self.salidaConsolaWeb)
                temporalMBR.doDeserialize(datos) #ya tenemos los datos del mbr
                self.temporalMBR = temporalMBR
                listaParticiones = [self.temporalMBR.particion1,self.temporalMBR.particion2, self.temporalMBR.particion3, self.temporalMBR.particion4]
                tamanoMBR = self.temporalMBR.mbr_tamano
                fechacreacionMBR = self.temporalMBR.mbr_fecha_creacion
                asignatureMBR = self.temporalMBR.mbr_dsk_signature        
                salida="""
                digraph G {
                a1 [shape=none label=<
                <TABLE cellspacing="10" cellpadding="10" 
                style="rounded" bgcolor="red">
                <TR>
                <TD bgcolor="yellow">REPORTE MBR</TD>
                </TR>
                <TR>
                <TD bgcolor="yellow">mbr_tamano</TD>"""
                salida +=f"<TD bgcolor=\"yellow\">{tamanoMBR}</TD>"
                salida +=f"""
                </TR>
                <TR>
                <TD bgcolor="yellow">mbr_fecha_creacion</TD>
                <TD bgcolor="yellow">{fechacreacionMBR}</TD>
                </TR>
                
                <TR>
                <TD bgcolor="yellow">mbr_disk_signature</TD>
                <TD bgcolor="yellow">{asignatureMBR}</TD>
                </TR>
                <TR>
                <TD bgcolor="purple">Particion</TD>
                </TR>
                """
                for particion in listaParticiones:
                    if particion.part_type == "E":
                        ebr_start = particion.part_start
                        salida +=f"""
                        <TR>
                        <TD bgcolor="yellow"> part status </TD>
                        <TD bgcolor="yellow"> {particion.part_status} </TD>
                        </TR>
                        
                        <TR>
                        <TD bgcolor="yellow"> part type </TD>
                        <TD bgcolor="yellow"> {particion.part_type} </TD>
                        </TR>
                        
                        <TR>
                        <TD bgcolor="yellow"> part fit </TD>
                        <TD bgcolor="yellow"> {particion.part_fit} </TD>
                        </TR>
                        
                        <TR>
                        <TD bgcolor="yellow"> part start </TD>
                        <TD bgcolor="yellow"> {particion.part_start} </TD>
                        </TR>
                        
                        <TR>
                        <TD bgcolor="yellow"> part size </TD>
                        <TD bgcolor="yellow"> {particion.part_s} </TD>
                        </TR>
                        
                        <TR>
                        <TD bgcolor="yellow"> part name </TD>
                        <TD bgcolor="yellow"> {particion.part_name} </TD>
                        </TR>
                        
                        """
                        while True:
                            actualEBR = EBR()
                            tamanioEBR = struct.calcsize(actualEBR.constanteEBR)
                            datosEBR = Fread_displacement(direccion, ebr_start, tamanioEBR,self.salidaConsolaWeb)
                            actualEBR.doDeserialize(datosEBR)
                            salida +=f""" 
                            <TR>
                            <TD bgcolor="purple">Particion Logica</TD>
                            </TR>
                            """
                            if actualEBR.part_status == "1":
                                salida +=f"""
                                <TR>
                                <TD bgcolor="yellow"> part status </TD>
                                <TD bgcolor="yellow"> {actualEBR.part_status} </TD>
                                </TR>
                                
                                <TR>
                                <TD bgcolor="yellow"> part next </TD>
                                <TD bgcolor="yellow"> {actualEBR.part_next} </TD>
                                </TR>
                                
                                <TR>
                                <TD bgcolor="yellow"> part fit </TD>
                                <TD bgcolor="yellow"> {actualEBR.part_fit} </TD>
                                </TR>
                                
                                <TR>
                                <TD bgcolor="yellow"> part start </TD>
                                <TD bgcolor="yellow"> {actualEBR.part_start} </TD>
                                </TR>
                                
                                <TR>
                                <TD bgcolor="yellow"> part size </TD>
                                <TD bgcolor="yellow"> {actualEBR.part_s} </TD>
                                </TR>
                                
                                <TR>
                                <TD bgcolor="yellow"> part name </TD>
                                <TD bgcolor="yellow"> {actualEBR.part_name} </TD>
                                </TR>
                                """
                            if actualEBR.part_next == -1:
                                break  # No hay más EBRs en la partición extendida
                            ebr_start = actualEBR.part_next  #Siguiente EBR
                    elif particion.part_status == "1":
                        salida +=f"""
                        <TR>
                        <TD bgcolor="purple">Particion</TD>
                        </TR>
                        
                        <TR>
                        <TD bgcolor="yellow"> part status </TD>
                        <TD bgcolor="yellow"> {particion.part_status} </TD>
                        </TR>
                        
                        <TR>
                        <TD bgcolor="yellow"> part type </TD>
                        <TD bgcolor="yellow"> {particion.part_type} </TD>
                        </TR>
                        
                        <TR>
                        <TD bgcolor="yellow"> part fit </TD>
                        <TD bgcolor="yellow"> {particion.part_fit} </TD>
                        </TR>
                        
                        <TR>
                        <TD bgcolor="yellow"> part start </TD>
                        <TD bgcolor="yellow"> {particion.part_start} </TD>
                        </TR>
                        
                        <TR>
                        <TD bgcolor="yellow"> part size </TD>
                        <TD bgcolor="yellow"> {particion.part_s} </TD>
                        </TR>
                        
                        <TR>
                        <TD bgcolor="yellow"> part name </TD>
                        <TD bgcolor="yellow"> {particion.part_name} </TD>
                        </TR>
                        """
                salida += """\n
                </TABLE>>];
                }
                """
                graph = graphviz.Source(salida)
                extencion = self.nombreArchivo.split(".")
                graph.format = "svg"
                graph.render(extencion[0],directory="./static/images")
                return
        self.salidaConsolaWeb.append(f"No se encontro el Disco")
    
    
    def crearGrafoDisk(self, listaMount):
        direccion = ""
        for identificadores in listaMount:
            if identificadores['id'] == self.identificador:
                direccion = identificadores['path']
                particion = identificadores['particion']
                temporalMBR = MBR(0, 0, 0, 0)
                datos = Fread_displacement(direccion, 0, struct.calcsize(temporalMBR.constMBR) + struct.calcsize(temporalMBR.particion1.constanteParticion) * 4,self.salidaConsolaWeb)
                temporalMBR.doDeserialize(datos)  # ya tenemos los datos del MBR
                self.temporalMBR = temporalMBR
                listaParticiones = [self.temporalMBR.particion1, self.temporalMBR.particion2, self.temporalMBR.particion3, self.temporalMBR.particion4]
                totalDisco = self.temporalMBR.mbr_tamano
                espacioUsado = 0
                espacioLibre = totalDisco  # Inicialmente, el espacio libre es igual al tamaño total del disco
                
                # Inicializa la variable de salida
                salida = """
                digraph D {
                    subgraph cluster_0 {
                        bgcolor="#68d9e2"
                        node [style="rounded" style=filled];
                """
                # Inicializa el contador de particiones lógicas dentro de la partición extendida
                num_particiones_logicas = 0
                for particion in listaParticiones:
                    if particion.part_status == "1":
                        salida += f"""
                        node_{particion.part_name} [label="{particion.part_name}\\nTipo: {particion.part_type}\\nTamaño: {particion.part_s} bytes\\nPorcentaje: {(particion.part_s * 100) / totalDisco}%"]
                        """
                        espacioUsado += particion.part_s
                        espacioLibre -= particion.part_s
                        
                        if particion.part_type == "E":
                            # Si es una partición extendida, muestra sus particiones lógicas
                            ebr_start = particion.part_start
                            while True:
                                actualEBR = EBR()
                                tamanioEBR = struct.calcsize(actualEBR.constanteEBR)
                                datosEBR = Fread_displacement(direccion, ebr_start, tamanioEBR,self.salidaConsolaWeb)
                                actualEBR.doDeserialize(datosEBR)
                                if actualEBR.part_status == "1":
                                    num_particiones_logicas += 1
                                    salida += f"""
                                    node_{particion.part_name}_logica{num_particiones_logicas} [label="{actualEBR.part_name}\\nTamaño: {actualEBR.part_s} bytes\\nPorcentaje: {(actualEBR.part_s * 100) / totalDisco}%"]
                                    """
                                if actualEBR.part_next == -1:
                                    break  # No hay más EBRs en la partición extendida
                                ebr_start = actualEBR.part_next  # Siguiente EBR
                
                # Agrega información del espacio libre
                salida += f"""
                node_Libre [label="Espacio Libre\\nTamaño: {espacioLibre} bytes\\nPorcentaje: {(espacioLibre * 100) / totalDisco}%"]
                """
                
                # Cierra la definición del grafo
                salida += """
                    }
                }
                """
                
                # Crea y muestra el grafo DOT
                graph = graphviz.Source(salida)
                extencion = self.nombreArchivo.split(".")
                graph.format = "svg"
                graph.render(extencion[0],directory="./static/images")
                return
        self.salidaConsolaWeb.append(f"No se encontro el Disco")
    # Asegúrate de que la función tenga acceso a las definiciones de MBR, Fread_displacement, y EBR según tu implementación actual.

                    