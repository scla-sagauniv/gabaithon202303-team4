from urllib import request, parse
import base64
import json
import uuid

def print_res_from_req(req):
    response = request.urlopen(req)
    result = response.read()
    print(result.decode())
    return result.decode()
  
base_url = "https://api.steinhq.com/v1/storages/6400a08feced9b09e9c1efc9"
auth_info = 'Yamato:Yamato200113'
basic_auth_token = base64.b64encode(auth_info.encode()).decode()

table = 'images'
headers = {'Authorization': f'Basic {basic_auth_token}'}

#テーブルに挿入する
def insert(state):
    
    data = [{
        'uuid': str(uuid.uuid4()),
        'uid': state['uid'],
        'url': state['url'],
        'labels': state['labels'],
        'is_open_data': state['is_open_data']
    }]
    url = f'{base_url}/{table}'
    req = request.Request(url=url, headers=headers, data=json.dumps(data).encode())
    print_res_from_req(req=req)

    
    return 

# data= {
#     'uid': '12afafa',
#     'url': 'http://sagau.ac.jp',
#     'labels': 'cat',
#     'is_open_data': False
# }
# insert(data)


#テーブルからURLをとってくる
def fetch(uid):
    where = {"uid": uid }
    # print(where)
    where_encoded = parse.quote(json.dumps(where), safe=":/")
    url = f'{base_url}/{table}?search={where_encoded}'
    # print(url)
    req = request.Request(url=url, headers=headers)
    result = json.loads(print_res_from_req(req=req))
    # fetchURL = result[0]['url']
    return result

# uid = "12afafa"
# print(fetch(uid))
    
