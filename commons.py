from urllib import request, parse
import base64
import json
import os
from enum import Enum
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction, QuickReply
)


line_bot_api = LineBotApi(os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('LINE_CHANNEL_SECRET'))

LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
DB_API_BASE_URL = os.environ.get('DB_API_BASE_URL')
DB_AUTH_INFO = os.environ.get('DB_AUTH_INFO')
DB_BASIC_AUTH_TOKEN = base64.b64encode(DB_AUTH_INFO.encode()).decode()
DB_REQUEST_HEADERS = {'Authorization': f'Basic {DB_BASIC_AUTH_TOKEN}'}

#config.pyで設定したAzure Blob Storageの接続文字列
AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
#config.pyで設定したAzure Blob Storageのコンテナ名
AZURE_STORAGE_CONTAINER_NAME = os.environ.get('AZURE_STORAGE_CONTAINER_NAME')
AZURE_STORAGE_ACCOUNT_NAME = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME')

class TableName(Enum):
    USERS = 'users'
    IMAGES = 'images'
    LOCATIONS = 'locations'

class SetupStep(Enum):
    CREATE = 0
    LOCATION = 1
    EXEC_TIME = 2
    IS_PUBLIC_SEND = 3
    IS_OPEN_DATA = 4
    COMPLETE = 5

class PostbackEventAction(Enum):
    SETUP = 'setup'

def exec_api_request(req):
    '''
    urllibのrequest.Requestオブジェクトを渡すとレスポンスをdict型で返す関数

    Args:
        req: request.Request
    Returns:
        dict or None
    '''
    response = request.urlopen(req)
    result = response.read()
    map_data = json.loads(result.decode())
    return map_data

def create_quick_reply_message(text, item_list):
    '''
    item_listを選択肢としたクイックリプライメッセージを作成する関数

    Args:
        text: string
        item_list: List<any>
    Returns:
        TextSendMessage
    '''
    items = [QuickReplyButton(action=MessageAction(label=f"{item}", text=f"{item}")) for item in item_list]
    messages = TextSendMessage(text=text,
                               quick_reply=QuickReply(items=items))
    return messages