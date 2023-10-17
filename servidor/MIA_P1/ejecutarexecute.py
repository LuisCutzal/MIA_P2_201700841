class comandoExecute:
    def __init__(self,ruta,nombreArchivo):
        self.ruta=ruta
        self.nombreArchivo=nombreArchivo
            
    def ejecutar(self):        
        try:
            with open(self.ruta + self.nombreArchivo, "r") as archivo:
                data = archivo.read()
                return data
        except FileNotFoundError:
            print(f"El archivo '{self.nombreArchivo}' no existe.")
        except Exception as e:
            print(f"Error al leer objeto: {e}")