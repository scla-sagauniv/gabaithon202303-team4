import flask
from flask import Flask, request, abort, render_template
import config
import tempfile
from crud_images import insert,fetch
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    PostbackEvent, FollowEvent, MessageEvent, TextMessage, TextSendMessage,
    MessageEvent, TextMessage, TextSendMessage,ImageMessage,
)

from azure.storage.blob import (
  BlobServiceClient, BlobClient, ContainerClient
)
import os
from os.path import join, dirname
from dotenv import load_dotenv

from commons import *
from setup import setup
from exec_time import ExecTime

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)


@app.route("/", methods=['GET'])
def health_check():
    return 'OK'

@app.route("/locationSetting", methods=['GET'])
def location_setting():
    return render_template('/index.html')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = flask.request.headers['X-Line-Signature']

    # get request body as text
    body = flask.request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'setup':
        setup(event.source.user_id, SetupStep.CREATE.value)
        return
    if event.message.text in ExecTime().merge_list():
        setup(event.source.user_id, SetupStep.EXEC_TIME.value, event.message.text)
        return
    if(event.message.text == "画像を登録する"):
        reply_message = TextSendMessage(text = "画像を送信してください")
        line_bot_api.reply_message(
            event.reply_token,
            reply_message
        )
        return
    setup(event.source.user_id, SetupStep.LOCATION.value, event.message.text)
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))

@handler.add(PostbackEvent)
def on_postback(event):
    str_work_date = event.postback.data
    params = str_work_date.split('&')
    print(PostbackEventAction(params[0].split('=')[1]))
    if PostbackEventAction(params[0].split('=')[1]) == PostbackEventAction.SETUP:
        print(params[1].split('=')[1], params[2].split('=')[1], params[3].split('=')[1])
        setup(params[1].split('=')[1], int(params[2].split('=')[1]), params[3].split('=')[1])
        

@handler.add(FollowEvent)
def follow_message(event):
    message = "フォローありがとう!\n今から初期設定をしてもらうね!"
    if event.type == "follow":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )
        # setup(event.source.user_id, SetupStep.CREATE.value)

# 画像を保存してメッセージを返す
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
  if event.reply_token == "00000000000000000000000000000000":
    return
  # # LINE Messaging APIからの画像をAzure Blob Storageに保存する
  message_id = event.message.id
  message_content = line_bot_api.get_message_content(message_id)

  #uidの取得
  uid = event.source.user_id


  # Azure Storage SDKの初期化
  blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
  container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)

  #一時ファイルの生成
  _, temp_local_filename = tempfile.mkstemp()

  tmp = b""
  with open(temp_local_filename, 'wb') as fd:
    for chunk in message_content.iter_content():
      # fd.write(chunk)
      tmp += chunk
  #保存するファイルの名前
  file_name = f"{message_id}.jpg"
  blob_client = container_client.get_blob_client(file_name)
  blob_client.upload_blob(tmp, overwrite=True)
  os.remove(temp_local_filename)

  contenturl = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_STORAGE_CONTAINER_NAME}/{file_name}"

  data = {
    'uid': uid,
    'url': contenturl,
    'labels': '',
  }
  insert(data)

  #公開範囲を訪ねる
  # line_bot_api.reply_message(
  #   event.reply_token,
  #   TextMessage("公開範囲を決めてください")
  # )

  #とってくる画像のパス
  blob_client = container_client.get_blob_client(file_name)
  # image_data = blob_client.download_blob().readall()
  reply_message = TextSendMessage(text = "画像を登録しました")
  #LineBotAPIに送信
  line_bot_api.reply_message(
    event.reply_token,
    reply_message
  )



if __name__ == "__main__":
    app.run(port=8000)
