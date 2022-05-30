import requests


def get_weather(command):
    appid = '1e21c100bda32fd7e80f329a1821a91f'
    for i in command.split(" "):
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': i+",RU", 'type': 'like', 'units': 'metric', 'APPID': appid})
            check = 1
        except Exception:
            check = 0
    if command == "погода":
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': "Красноярск,RU", 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        city_id = data['list'][0]['id']
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        weather = {'city': cities[0],
                   'temperature': str(data['main']['temp']) + "°C",
                   'feels_like': str(int(data['main']['feels_like'])) + "°C",
                   'wind': str(int(data['wind']['speed'])) + "м/с",
                   'humidity': str(data['main']['humidity']) + "%",
                   'status': data['weather'][0]['description']
                   }
        return weather
    
    elif check == 1:
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        city_id = data['list'][0]['id']
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        weather = {'city': cities[0],
                   'temperature': str(data['main']['temp']) + "°C",
                   'feels_like': str(int(data['main']['feels_like'])) + "°C",
                   'wind': str(int(data['wind']['speed'])) + "м/с",
                   'humidity': str(data['main']['humidity']) + "%",
                   'status': data['weather'][0]['description']
                   }
        return weather
    else:
        return 0
