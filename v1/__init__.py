from .openweather import open_weather
from .auth import auth

def register_v1(app):
    app.register_blueprint(open_weather)
    app.register_blueprint(auth)