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

def convertirValoresFit(valorFit):
    if valorFit == "BF":
        return "B"
    elif valorFit == "FF":
        return "F"
    elif valorFit == "WF":
        return "W"
    else: print(f"el valor {valorFit} de fit no es valido")
    
    
def ejecutarPause():
    print("pause")