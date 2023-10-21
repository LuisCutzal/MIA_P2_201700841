from flask import Flask, jsonify, request, url_for
from flask_cors import CORS  
from MIA_P1.readData import readData
import os
app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return jsonify({'message': 'Hello, World!'})


@app.route("/api", methods=['POST'])
def execute():
    try:
        data = request.get_json()
        entry_value = data.get('entry')
    except:
        # Si no se pudo obtener JSON, asumir que es texto plano y tomarlo directamente del cuerpo de la solicitud
        entry_value = request.data.decode('utf-8')

    response = readData(entry_value)
    return jsonify({'salida': response})

@app.route("/api/getImages", methods=['GET'])
def get_images():
    dir_imagen = 'static/images'  # Nombre de la carpeta de imágenes
    array_Imagen = []
    listaImagen=  os.listdir(dir_imagen)
    for urlimagen in listaImagen:
        direccionImagen = url_for('static', filename = 'images/'+urlimagen, _external = True)
        array_Imagen.append({
            "nombre": os.path.basename(urlimagen),
            "direccion":direccionImagen
        })
    return jsonify(array_Imagen)

if __name__ == '__main__':
    app.run()