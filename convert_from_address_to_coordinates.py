import requests


class GetCoords:
    api_url = 'https://geocode-maps.yandex.ru/1.x/'

    def __init__(self, api_key: str):
        self.api_key = api_key

    def send_request(self, data: str):
        r = requests.get(self.api_url,
                         params=dict(format='json',
                                     apikey=self.api_key,
                                     geocode=data))

        if r.status_code == 200:
            return r.json()['response']
        elif r.status_code == 403:
            print('Такого адреса|координат не существует')
        else:
            print('Что-то пошло не так, но не из-за адреса')

    def get_coords_by_address(self, address: str):
        coords = self.send_request(address)['GeoObjectCollection']['featureMember']

        # Если ответ пустой, то «поднимаем» ошибку
        if not coords:
            print('Пустой ответ')
        try:
            coords = coords[0]['GeoObject']['Point']['pos']
            lon, lat = coords.split(' ')
            return float(lon), float(lat)
        except IndexError:
            return

#
# api_key = '5cbf1bfd-9264-477c-b05c-2af092e99e54'
# example = GetCoords(api_key)
# address = 'Гашека 7'
# print(example.get_coords_by_address(address))
