from .openweather import open_weather

def register_v1(app):
    app.register_blueprint(open_weather)