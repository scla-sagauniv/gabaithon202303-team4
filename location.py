from urllib import request, parse

from commons import *

class Locations:
    def fetch_all():
        '''
        DBに登録されている全てのLocationを取得する

        Returns:
            List<Location>
        '''
        url = f'{DB_API_BASE_URL}/{TableName.LOCATIONS.value}'
        req = request.Request(url=url, headers=DB_REQUEST_HEADERS)
        all_locations = exec_api_request(req=req)
        return list(map(Location.from_dict_data, all_locations))


class Location:
    def __init__(self, area_code, weather_index, temperature_index, label):
        '''
        *注意* 全てstring

        Args:
            area_code: string
            index: string
            label: string
        '''
        self.area_code = area_code
        self.weather_index = weather_index
        self.temperature_index = temperature_index
        self.label = label
    
    def from_dict_data(dict_data):
        '''
        jsonから変換したdictからLocationを生成する

        Args:
            dict_data: dict<'area_code', 'index', 'label'>
        Rerturns:
            Location
        '''
        return Locations(dict_data['area_code'], dict_data['weather_index'], dict_data['temperature_index'], dict_data['label'])
    
    def from_label(label):
        '''
        labelでlocationsテーブルをサーチして、結果をLocationにして返す

        Args:
            label: string
        Returns:
            Location
        '''
        where = {'label': label}
        print(f'hgohoe:::{label}')
        query_param = parse.quote(json.dumps(where), safe=":/")
        url = f'{DB_API_BASE_URL}/{TableName.LOCATIONS.value}?search={query_param}'
        req = request.Request(url=url, headers=DB_REQUEST_HEADERS)
        res = exec_api_request(req=req)[0]
        return Location(res['area_code'], res['weather_index'], res['temperature_index'], res['label'])
