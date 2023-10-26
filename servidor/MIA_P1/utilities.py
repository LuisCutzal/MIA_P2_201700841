import random
import math
import datetime

def coding_str(string,size):
    return string.encode('utf-8')[:size].ljust(size, b'\0')


def convertirstringaBin(string):
    return string.encode()


def randomVal(inicio, fin):
    return math.floor(random.uniform(inicio, fin))

def tiempo():
    valorTiempo = datetime.datetime.now() #devuelve fecha y hora, se puede combertir en string, entero y volverlo a descombertir
    return int(valorTiempo.timestamp()) #esto se puede transformar en binario y volverlo a transformar a int


def convertirFecha(fecha):
    return datetime.datetime.fromtimestamp(fecha)

def convertirTiempoEntero(fecha):
    return int(fecha.timestamp())


def deBinaString(datoBinario):
    return datoBinario.decode().rstrip('\x00')

def convertirValoresFit(valorFit,salidaConsolaWeb):
    if valorFit.lower() == "bf":
        return "B"
    elif valorFit.lower() == "ff":
        return "F"
    elif valorFit.lower() == "wf":
        return "W"
    else: salidaConsolaWeb.append(f"el valor {valorFit} de fit no es valido")
    
    
def ejecutarPause(salidaConsolaWeb):
    salidaConsolaWeb.append("pause")