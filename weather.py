from pyowm import OWM
from pyowm.utils.config import get_default_config


def get_weather(command):
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = OWM('1e21c100bda32fd7e80f329a1821a91f', config_dict)
    mgr = owm.weather_manager()
    for i in command.split(" "):
        try:
            observation = mgr.weather_at_place(place+",RU")
        except Exception:
            place = 0  # Города не существует
        finally:
            place = i
    if place == 0:
        return 0
    observation = mgr.weather_at_place(place + ",RU")
    w = observation.weather
    t = w.temperature("celsius")
    weather = {	'city': place,
                'temperature': str(int(t['temp']+0.5))+"°C", 
                'feels_like': str(int(t['feels_like']+0.5))+"°C",
                'wind': str(int(w.wind()['speed']+0.5))+"м/с",
                'humidity': str(w.humidity) + "%",
                'status': w.detailed_status
                }
    return weather