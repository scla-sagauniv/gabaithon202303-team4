import config
from flask import Flask, request, abort

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

app = Flask(__name__)

#config.pyで設定したチャネルアクセストークン
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN) 

#config.pyで設定したチャネルシークレット
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
  #signature: 署名
  #Webhookリクエストに含まれる署名を取得
  signature = request.headers['X-Line-Signature']

  #ペイロードを取得
  body = request.get_data(as_text=True)
  app.logger.info("Request body" + body)

  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    print("Invalid signature. Please check your channel access token/channel secret.")
    abort(400)
  return 'OK'

