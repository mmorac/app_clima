from flask import Blueprint, jsonify, request
import requests as rq
from datetime import datetime

open_weather = Blueprint('open_weather', __name__)

baseURL = '/v1/weather/'

#Esto es muy similar a los atributos de los métodos del controlador en C#
#Se agrega tanto el método como el path
@open_weather.route(baseURL + 'test', methods = ['GET'])
def weather_test():
    return jsonify({'result': 'True', 'response': 'Primer endpoint con flask y todo salió tuanis.'})

@open_weather.route(baseURL + '7dias/<ciudad>', methods = ['GET'])
def weather_in(ciudad):
    try:
        info = rq.get(f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=ierqQnKPN6Q1O0vK9dnENMuAIaf6lkA5&q={ciudad}').json()
        ciudad_id = info[0]["Key"]
        clima = rq.get(f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{ciudad_id}?apikey=ierqQnKPN6Q1O0vK9dnENMuAIaf6lkA5')
        fechas = clima.json()['DailyForecasts']
        pronostico = []
        for f in fechas:
            lista = [f["Date"], f_to_c(f["Temperature"]["Maximum"]["Value"]), f_to_c(f["Temperature"]["Maximum"]["Value"]), f["Day"]["IconPhrase"]]
            pronostico.append(lista)
        return jsonify({'result': 'True', 'response': f'La información para {ciudad} es: {pronostico}'}), 200
    except Exception as e:
        print(e)
        return jsonify({'result': 'False', 'response': 'Ha ocurrido un error en tu solicitud.'}), 500


@open_weather.route(baseURL + '7dias', methods = ['POST'])
def weather_in_post():
    inData = request.get_json()     
    try:
        return jsonify({'result': 'True', 'response': f'El clima para 7 días en {inData["ciudad"]} es:'}), 200
    except Exception as e:
        print(e)
        return jsonify({'result': 'False', 'response': 'Hay un error en este request'}), 500


def f_to_c(temp):
    return round((temp - 32) * (5/9), 2)

def mph_to_kph(velocidad):
    return round(velocidad / 1.609, 2)