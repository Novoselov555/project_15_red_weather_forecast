from flask import Flask, render_template, request
from weather_receiver import WeatherReceiver, weather_key_parameters
from convert_from_address_to_coordinates import GetCoords

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    cities = request.form.getlist('cities[]')
    ans = []
    for city in cities:
        try:
            lon, lat = GetCoords(api_location_to_coords).get_coords_by_address(city)
            WeatherReceiver(api_for_weather).get_weather(lat, lon)
            weather_data = weather_key_parameters()
            for i in range(len(weather_data)):
                data = weather_data[i]
                # Дневные параметры
                day_temp = data['max_temp']
                day_rain = data['day_forecast']['rain_probability']
                day_humidity = data['day_forecast']['humidity']
                day_wind = data['day_forecast']['wind_speed']
                # Ночные параметры
                night_temp = data['min_temp']
                night_rain = data['night_forecast']['rain_probability']
                night_humidity = data['night_forecast']['humidity']
                night_wind = data['night_forecast']['wind_speed']

                params = {
                    'city_name': city,
                    'day_temp': day_temp,
                    'day_rain': day_rain,
                    'day_humidity': day_humidity,
                    'day_wind': day_wind,
                    'night_temp': night_temp,
                    'night_rain': night_rain,
                    'night_humidity': night_humidity,
                    'night_wind': night_wind,
                }
                ans.append(params)

        except Exception as e:
            print(f"Ошибка обработки города {city}: {str(e)}")

    print(ans)

    return render_template('result.html', data=ans)


api_location_to_coords = '5cbf1bfd-9264-477c-b05c-2af092e99e54'
api_for_weather = 'AGlRoTK491bc73SZrvSPGGx6fisQS586'
if __name__ == '__main__':
    app.run(debug=True)