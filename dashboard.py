import plotly.express as px
import pandas as pd
import json

def generate_graphs():
    # Загружаем данные о погоде
    with open('weather_key_parameters.json', 'r') as file:
        weather_data = json.load(file)

    df = pd.DataFrame(weather_data)
    df['date'] = pd.to_datetime(df['date'])  # Преобразуем дату

    # Построение графика температуры
    fig_temp = px.line(
        df,
        x='date',
        y=['max_temp', 'min_temp'],
        labels={'value': 'Температура (°C)', 'date': 'Дата'},
        title='Температурный прогноз на несколько дней'
    )

    # Построение графика вероятности дождя
    fig_rain = px.bar(
        df,
        x='date',
        y=[df['day_forecast'].apply(lambda x: x['rain_probability']),
           df['night_forecast'].apply(lambda x: x['rain_probability'])],
        labels={'value': 'Вероятность дождя (%)', 'date': 'Дата'},
        title='Вероятность дождя на несколько дней'
    )
    fig_rain.update_layout(barmode='group', xaxis_tickangle=-45)

    # Генерация HTML для вставки в шаблон
    temp_html = fig_temp.to_html(full_html=False)
    rain_html = fig_rain.to_html(full_html=False)

    return temp_html, rain_html
