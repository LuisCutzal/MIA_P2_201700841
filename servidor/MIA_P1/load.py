import ctypes
import os
def leerArchivo(archivo): #para el path del archivo de entrada 
    try:
        data = archivo.read()
        archivo.close()
        return data
    except Exception as e:
        print(f"Error al leer archivo: {e}")

   
def Fread_displacement(path, displacement, size): #desplazamiento -> cuanto se desplaza el puntero sieze-> cuantos bites debemos leer
    try:
        with open(path, "rb+") as file:
            file.seek(int(displacement))
            data = file.read(size)
            return data #cantidad en bytes que leimos
    except Exception as e:
        print(f"Error al leer archivo: {e}")
        

def Fwrite_displacement(file, displacement, data): #este data es bites
    file.seek(displacement)
    file.write(data)

def Fcreate_file(fileName):
    try:
        # Divide la ruta en carpetas y nombre de archivo
        folder, file_name = os.path.split(fileName)
        # Crea las carpetas necesarias si no existen
        if folder:
            os.makedirs(folder, exist_ok=True)
        # Crea el archivo
        fileOpen = open(fileName, "wb")
        fileOpen.close()
        print("Archivo creado exitosamente")
        return False
    except Exception as e:
        print(f"Error al crear archivo: {e}")
        return True

def Winit_size(file, size_mb):
    buffer = b'\0' * size_mb
    print(f"Tamaño del archivo: {len(buffer)} bytes")
    file.write(buffer)
    print("Tamaño aplicado")


def archivoExistente(file):
    if os.path.exists(file):
        return True


def escribirArchivoExistente(path, displacement, data):
    try:
        with open(path, "rb+") as file:
            file.seek(displacement)
            file.write(data)
    except IOError:
        print("Error al escribir la particion")
        return
    