from flask import Flask, jsonify, request
from flask_cors import CORS  
from MIA_P1.readData import readData

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

if __name__ == '__main__':
    app.run()