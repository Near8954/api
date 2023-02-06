import sys
from io import BytesIO

import requests
from PIL import Image


def calc_spn(toponym):
    lower = [float(elem) for elem in toponym['boundedBy']['Envelope']['lowerCorner'].split()]
    upper = [float(elem) for elem in toponym['boundedBy']['Envelope']['upperCorner'].split()]

    delta1 = str(abs(upper[0] - lower[0]) / 2)
    delta2 = str(abs(upper[1] - lower[1]) / 2)
    return delta1, delta2


toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = "0.005"
print(calc_spn(toponym))
# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join(calc_spn(toponym)),
    "l": "sat",
    'pt': f'{toponym_longitude},{toponym_lattitude},home'
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
