import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # 上のディレクトリに移動
import config # config.pyファイルをインポート

from flask import Flask, request, abort
from get_img_access import get_img_access #出力される画像が自分のだけがいいか他のも許可するか
from region import region #天気を知りたい地域
from set_public_access import set_public_access #ユーザーが入力した画像の公開範囲
from response_time import response_time #ユーザーが入力した通知の時間（よゆうがあれば）


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
  FollowEvent
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

# @handler.add(MessageEvent, message=TextMessage)
@handler.add(FollowEvent)
def initial_settings(event):
  # 友達に追加されたときに表示したい
  

  region(event)

  set_public_access(event)

  get_img_access(event)





if __name__ == "__main__":
  app.run(host="localhost", port = 8000)