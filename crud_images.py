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
    uuid = str(uuid.uuid4())
    data = [{
        'uuid': uuid,
        'uid': state['uid'],
        'url': state['url'],
        'labels': state['labels'],
    }]
    url = f'{base_url}/{table}'
    req = request.Request(url=url, headers=headers, data=json.dumps(data).encode())
    print_res_from_req(req=req)

    
    return uuid

# data= {
#     'uid': '12afafa',
#     'url': 'http://sagau.ac.jp',
#     'labels': 'cat'
# }
# insert(data)


#テーブルからURLをとってくる
def fetch(url):
    where = {"url": url }
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

def update_images(data):
    where = {'uuid': data['uuid']}
    value = {'labels': data['labels']}
    data = { 'condition': where, 'set': value }
    url = f'{base_url}/{table}'
    req = request.Request(url=url, headers=headers, data=json.dumps(data).encode(), method='PUT')
    print_res_from_req(req=req)
    return 

# data= {
#     'uuid': 'b03f8ad8-386e-44aa-8ff0-47de4b0ec722',
#     'labels': 'fox'
# }
# update_images(data)
