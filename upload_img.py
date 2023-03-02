import config
from flask import Flask, request, abort
import tempfile
import os
import urllib.request

#Lineメッセージングプラットフォーム上でチャットボットを構築するためのライブラリであるLine Messaging API SDKで提供されるクラス
from linebot import (
  LineBotApi, WebhookHandler
)

#Webhookへのリクエストの署名が無効な場合に発生する
from linebot.exceptions import (
  InvalidSignatureError
)

#送受信できるメッセージ
from linebot.models import (
  MessageEvent, TextMessage, TextSendMessage, ImageMessage,ImageSendMessage
)

from azure.storage.blob import (
  BlobServiceClient, BlobClient, ContainerClient
)



#config.pyで設定したチャネルアクセストークン
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN) 

#config.pyで設定したチャネルシークレット
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

#config.pyで設定したAzure Blob Storageの接続文字列
AZURE_STORAGE_CONNECTION_STRING = config.AZURE_STORAGE_CONNECTION_STRING

#config.pyで設定したAzure Blob Storageのコンテナ名
AZURE_STORAGE_CONTAINER_NAME = config.AZURE_STORAGE_CONTAINER_NAME

AZURE_STORAGE_ACCOUNT_NAME = config.AZURE_STORAGE_ACCOUNT_NAME

def register_img(event):
  ##LINE Messaging APIからの画像をAzure Blob Storageに保存する
  message_id = event.message.id

  message_content = line_bot_api.get_message_content(message_id)

  # Azure Storage SDKの初期
  blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
  container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)

  #一時ファイルの生成
  _, temp_local_filename = tempfile.mkstemp()

  tmp = b""
  with open(temp_local_filename, 'wb') as fd:
    for chunk in message_content.iter_content():
      # fd.write(chunk)
      tmp += chunk
  
  file_name = f"{message_id}.jpg"
  #保存するファイルの名前
  blob_client = container_client.get_blob_client(file_name)
  blob_client.upload_blob(tmp, overwrite=True)
  os.remove(temp_local_filename)

  #画像をクライアントに送り返す
  # 今回は画像をオウム返しするのでfile_nameとなっているが、本番ではDBからとってくる
  blob_client = container_client.get_blob_client(file_name)
  image_data = blob_client.download_blob().readall()
  contenturl = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_STORAGE_CONTAINER_NAME}/{file_name}"
  print(contenturl)
  image_message = ImageSendMessage(original_content_url=f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_STORAGE_CONTAINER_NAME}/{file_name}", preview_image_url=f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_STORAGE_CONTAINER_NAME}/{file_name}")

  #LineBotAPIに送信
  # line_bot_api.reply_message(
  #   event.reply_token,
  # )
    