from flask import Flask, render_template, request
from weather_receiver import WeatherReceiver, weather_key_parameters
from convert_from_address_to_coordinates import GetCoords
from dashboard import generate_graphs
import json
import subprocess

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    cities = request.form.getlist('cities[]')
    with open('selected_cities.json', 'w', encoding='utf-8') as file:
        json.dump(cities, file, ensure_ascii=False)

    subprocess.run(['python', 'map_route.py'])
    ans = []
    for city in cities:
        try:
            lon, lat = GetCoords(api_location_to_coords).get_coords_by_address(city)
            WeatherReceiver(api_for_weather).get_weather(lat, lon)
            weather_data = weather_key_parameters()
            for data in weather_data:
                params = {
                    'city_name': city,
                    'day_temp': data['max_temp'],
                    'day_rain': data['day_forecast']['rain_probability'],
                    'day_humidity': data['day_forecast']['humidity'],
                    'day_wind': data['day_forecast']['wind_speed'],
                    'night_temp': data['min_temp'],
                    'night_rain': data['night_forecast']['rain_probability'],
                    'night_humidity': data['night_forecast']['humidity'],
                    'night_wind': data['night_forecast']['wind_speed'],
                }
                ans.append(params)
        except Exception as e:
            return render_template('error.html', message="Такого города не существует")

    # Получаем HTML графиков из dashboard
    temp_graph, rain_graph = generate_graphs()

    return render_template('result.html', data=ans, temp_graph=temp_graph, rain_graph=rain_graph)


api_location_to_coords = '5cbf1bfd-9264-477c-b05c-2af092e99e54'
api_for_weather = 'MlS1rPJXAFXJCzOHAUYzwB9YEX0r3Im7'

if __name__ == '__main__':
    app.run(debug=True)
