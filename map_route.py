import folium
from folium.plugins import AntPath
import requests
import json

# Функция для получения координат города
def get_coords(city):
    api_key = '97fc9f22b03e417267b5731c5c24c83a'
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}'
    response = requests.get(url)
    data = response.json()[0]
    return data['lat'], data['lon']

# Загружаем список городов из JSON
with open('selected_cities.json', 'r') as file:
    cities = json.load(file)

coordinates = []
weather_info = []

# Получаем координаты и погоду для каждого города
for city in cities:
    lat, lon = get_coords(city)
    coordinates.append((lat, lon))
    weather_info.append((city, lat, lon))

# Создаем карту, центрируя на первом городе
m = folium.Map(location=coordinates[0], zoom_start=5)

# Добавляем маркеры для каждого города с всплывающим текстом
for city, lat, lon in weather_info:
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{city}</b><br>Координаты: {lat:.2f}, {lon:.2f}",
        icon=folium.Icon(color='blue', icon='cloud')
    ).add_to(m)

# Добавляем линию маршрута между городами
AntPath(locations=coordinates, weight=5, color='blue').add_to(m)

# Сохраняем карту как HTML
m.save('static/route_map.html')
