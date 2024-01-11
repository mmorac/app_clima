import jwt, datetime
from flask import Blueprint, jsonify, request
from functools import wraps

secreto = 'NadaDeNada'

def fence(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            jwt_token = request.headers['Authorization']
            if jwt_token:
                resp = auth.check_jwt(jwt_token.split(' ')[1])
                if resp['result']:
                    return f(*args, **kwargs)
                else:
                    return jsonify({'result': False, 'response': resp}), 401
            else:
                return jsonify({'result': False, 'response': 'No se ha enviado el token'}), 401
        except Exception as e:
            return jsonify({'result': False, 'response': f"Error de solicitud: {e}"}), 401
    
           
    return decorator


class auth:

    def issue_jwt(_user):
        payload = {
            'user': _user["name"],
            'city': _user["city"],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow()
        }
        try:
            jwt_token = jwt.encode(payload, secreto, algorithm='HS256')
        except Exception as e:
            print("Excepción:", e)

        return jwt_token

    def check_jwt(_token):
        try:
            print("Intentando con:", _token)
            print("Y recibo:", jwt.decode(_token, secreto, algorithms=['HS256']))
            return {'result': True, 'response': jwt.decode(_token, secreto, algorithms=['HS256'])}
        except jwt.ExpiredSignatureError:
            return {'result': False, 'response': 'Token expirado'}
        except jwt.InvalidTokenError:
            return {'result': False, 'response': 'Token invalido'}
        
