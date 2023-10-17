from load import *
from ArchivoComandos import iniciarAnalisis

def aplicacionComandos():
    """input = iniciarAnalisis("execute -path=/home/luis/Escritorio/Archivos2023/proyectos/MIA_P1_201700841/prueba.dsk")
    #print(input)
    iniciarAnalisis(input)
    """
    while True: 
        #iniciarAnalisis(input("-> "))
        iniciamos = iniciarAnalisis(input("-> "))
        #print(input)
        iniciarAnalisis(iniciamos)

if __name__ == "__main__":
    print("Luis Antonio Cutzal Chalí")
    print("201700841")
    print("Proyecto 1")
    aplicacionComandos()