from flask import Blueprint, jsonify, request
from .utils import functions

auth = Blueprint('auth', __name__)

baseURL = '/v1/auth/'

usuario_demo = "test_user"
password_demo = "tyZB4fv7PcVzD1wMzC8T"

@auth.route(baseURL + 'test', methods = ['POST'])
def auth_test():
    try:
        inData = request.get_json()
        if(inData["usuario"] == usuario_demo and inData["password"] == password_demo):
            return jsonify({'result': 'True', 'response': 'Autenticación exitosa.'}), 200
        else:
            return jsonify({'result': 'False', 'response': 'Autenticación fallida.'}), 401
    except:
        return jsonify({'result': 'False', 'response': 'Error en la solicitud.'}), 400

@auth.route(baseURL + 'issuetoken', methods = ['POST'])
def issuetoken():
    try:
        try:
            inData = request.get_json()
        except Exception as e:
            print("Error:", e)
        token = functions.auth.issue_jwt(inData)
        return jsonify({'result': True, 'response': token}), 200
    except:
        return jsonify({'result': False, 'response': 'Ha ocurrido un error con la información provista.'}), 401