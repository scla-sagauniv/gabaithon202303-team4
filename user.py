from urllib import request, parse

from commons import *

class User:
    def __init__(self, uid, area_code='-1', is_public_send='-1', is_open_data='-1', exec_time='-1'):
        '''
        *注意* 全てstring
        
        Args:
            uid: string
            area_code: string
            is_public_send: string
            is_open_data: string
            exec_time: string
        '''
        self.uid = uid
        self.area_code = area_code
        self.is_public_send = is_public_send
        self.is_open_data = is_open_data
        self.exec_time = exec_time
    
    def from_dict_data(data):
        print(data)
        return User(data['uid'], data['area_code'], data['is_public_send'], data['is_open_data'], data['exec_time'])

    def to_dict_data(self):
        return {
            'uid': self.uid, 
            'area_code': self.area_code, 
            'is_public_send': self.is_public_send, 
            'is_open_data': self.is_open_data,
            'exec_time': self.exec_time
        }

    def create(self):
        '''
        ユーザーをDBにインサートする
        '''
        data = [self.to_dict_data()]
        print(data)
        url = f'{DB_API_BASE_URL}/{TableName.USERS.value}'
        print(url)
        req = request.Request(url=url, headers=DB_REQUEST_HEADERS, data=json.dumps(data).encode())
        exec_api_request(req=req)
    
    def update(self):
        '''
        ユーザーの情報を更新する
        '''
        where = {'uid': self.uid}
        value = self.to_dict_data()
        data = {'condition': where, 'set': value}
        url = f'{DB_API_BASE_URL}/{TableName.USERS.value}'
        req = request.Request(url=url, headers=DB_REQUEST_HEADERS, data=json.dumps(data).encode(), method='PUT')
        exec_api_request(req=req)
    
    def fetch_info_by_uid(uid):
        '''
        uidを元にUserの情報をDBからとってきてインスタンスにする

        Args:
            uid: string
        Returns:
            User
        '''
        where = {'uid': uid}
        query_param = parse.quote(json.dumps(where), safe=":/")
        url = f'{DB_API_BASE_URL}/{TableName.USERS.value}?search={query_param}'
        req = request.Request(url=url, headers=DB_REQUEST_HEADERS)
        res = exec_api_request(req=req)
        print(f'kokoo;{res}')
        return User.from_dict_data(res[0])
        

