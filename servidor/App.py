from flask import Flask, jsonify, request, url_for
from flask_cors import CORS
from MIA_P1.content import *
from MIA_P1.bloqueCarpeta import *
import os
from MIA_P1.ArchivoComandos import iniciarAnalisis
app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return jsonify({'message': 'Hello, World!'})


@app.route("/api", methods=['POST'])
def execute():
    salidaConsola = []
    try:
        data = request.get_json()
        entry_value = data.get('entry')
        salidaConsola =  iniciarAnalisis(entry_value)
    except:
        # Si no se pudo obtener JSON, asumir que es texto plano y tomarlo directamente del cuerpo de la solicitud
        entry_value = request.get_json()
        valor = entry_value.get('entry')
        salidaConsola =  iniciarAnalisis(valor)
    return jsonify({'salida': salidaConsola})

@app.route("/api/getImages", methods=['GET'])
def get_images():
    dir_imagen = 'static/images'  # Nombre de la carpeta de imágenes
    array_Imagen = []
    listaImagen=  os.listdir(dir_imagen)
    imagenes_jpg = [imagen for imagen in listaImagen if imagen.endswith('.svg')]
    for urlimagen in imagenes_jpg:
        direccionImagen = url_for('static', filename = 'images/'+urlimagen, _external = True)
        array_Imagen.append({
            "nombre": os.path.basename(urlimagen),
            "direccion":direccionImagen
        })
    return jsonify(array_Imagen)

    #UGO = user, group, other
def getpermission(permission):
    user_permission = permission//100
    group_permission = (permission%100)//10
    other_permission = permission%10
    print(user_permission, group_permission, other_permission)
    binary_permission = bin(user_permission)[2:].zfill(3)+bin(group_permission)[2:].zfill(3)+bin(other_permission)[2:].zfill(3)
    print(binary_permission)
    user_permission = binary_permission[:3]
    group_permission = binary_permission[3:6]
    other_permission = binary_permission[6:]
    user_permission = ['r' if user_permission[0] == '1' else '-', 'w' if user_permission[1] == '1' else '-', 'x' if user_permission[2] == '1' else '-']
    group_permission = ['r' if group_permission[0] == '1' else '-', 'w' if group_permission[1] == '1' else '-', 'x' if group_permission[2] == '1' else '-']
    other_permission = ['r' if other_permission[0] == '1' else '-', 'w' if other_permission[1] == '1' else '-', 'x' if other_permission[2] == '1' else '-']
    return user_permission, group_permission, other_permission

if __name__ == '__main__':
    app.run(debug=True)
    """contenido = content()
    contenido2 = content()
    contenido3 = content()
    contenido4 = content()
    contenido.set_valores('folder',1)
    contenido2.set_valores('folder2',2)
    contenido3.set_valores('folder3',3)
    contenido4.set_valores('folder4',4)
    blarpeta = bloqueCarpeta()
    blarpeta.set_valores([contenido,contenido2,contenido3,contenido4])
    #print(blarpeta.doSerialize())
    otro = blarpeta.doSerialize()
    contenidoCarpeta = blarpeta.doDeserialize(otro).b_content
    for i in contenidoCarpeta:
        print(i.b_inodo,i.b_name)"""
    #print(getpermission(755))
    
    
    