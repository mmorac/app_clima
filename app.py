from flask import Flask, request, jsonify
from v1 import register_v1

app = Flask(__name__)

register_v1(app)

if __name__ == '__main__':
    #Le indicamos a Flask qué ejecutar según el nombre de la app
    #Especificamos el host y el puerto (en este caso por ser local, se pone cualquier burrada)
    app.run(host='0.0.0.0', port=2024, debug=True)

