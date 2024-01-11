from flask import Blueprint, jsonify, request
import requests as rq
from datetime import datetime
from .utils import functions

open_weather = Blueprint('open_weather', __name__)

baseURL = '/v1/weather/'

#Esto es muy similar a los atributos de los métodos del controlador en C#
#Se agrega tanto el método como el path
@open_weather.route(baseURL + 'test', methods = ['GET'])
def weather_test():
    return jsonify({'result': 'True', 'response': 'Primer endpoint con flask y todo salió tuanis.'})

@open_weather.route(baseURL + 'ciudad')
def weather(ciudad):
    try:
        #Obtengo a través de la API el ID de la ciudad en el servicio de AccuWeather
        info = rq.get(f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=ierqQnKPN6Q1O0vK9dnENMuAIaf6lkA5&q={ciudad}').json()
        ciudad_id = info[0]["Key"]
        #Hago la solicitud del pronóstico para los próximos 5 días en la ciudad por key
        clima = rq.get(f'http://dataservice.accuweather.com/currentconditions/v1/{ciudad_id}?apikey=ierqQnKPN6Q1O0vK9dnENMuAIaf6lkA5').json()[0]
        #Creo una lista de listas conteniendo la información meteorológica para cada uno de los días solicitados
        pronostico = {"fecha": str(datetime.fromtimestamp(clima["EpochTime"])), "temperatura": clima["Temperature"]["Metric"]["Value"], "tiempo": clima["WeatherText"]}
        return jsonify({'result': 'True', 'response': pronostico}), 200
    except Exception as e:
        print("Error en la data:", e)
        return jsonify({'result': 'False', 'response': 'Ha ocurrido un error en tu solicitud.'}), 500

#Solicitar dinámicamente el clima de una ciudad para los próximos 5 días
#con base en el nombre de la ciudad, aportado en la URL
@open_weather.route(baseURL + '5dias/<ciudad>', methods = ['GET'])
@functions.fence
def weather_in(ciudad):
    try:
        #Obtengo a través de la API el ID de la ciudad en el servicio de AccuWeather
        info = rq.get(f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=ierqQnKPN6Q1O0vK9dnENMuAIaf6lkA5&q={ciudad}').json()
        ciudad_id = info[0]["Key"]
        #Hago la solicitud del pronóstico para los próximos 5 días en la ciudad por key
        clima = rq.get(f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{ciudad_id}?apikey=ierqQnKPN6Q1O0vK9dnENMuAIaf6lkA5')
        fechas = clima.json()['DailyForecasts']
        #Creo una lista de listas conteniendo la información meteorológica para cada uno de los días solicitados
        pronostico = []
        for f in fechas:
            lista = [f["Date"], f_to_c(f["Temperature"]["Maximum"]["Value"]), f_to_c(f["Temperature"]["Maximum"]["Value"]), f["Day"]["IconPhrase"]]
            pronostico.append(lista)
        return jsonify({'result': 'True', 'response': pronostico}), 200
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

@open_weather.route(baseURL + 'miciudad', methods=['POST'])
@functions.fence
def miciudad():
    try:
        inData = request.get_json()
        headerAuth = request.headers['Authorization']
        jwtData = functions.auth.check_jwt(headerAuth.split(' ')[1])['response']
        return weather(jwtData['city'])
    except Exception as e:
        return jsonify({'result': False, 'response': f'Peticion malformada - {str(e)}'}), 400        

