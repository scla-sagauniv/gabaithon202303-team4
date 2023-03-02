import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # 上のディレクトリに移動
import config # config.pyファイルをインポート
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

#config.pyで設定したチャネルアクセストークン
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN) 

#config.pyで設定したチャネルシークレット
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

#サーバ側で受信したメッセージの型が正しいか確認する
#正しければ

def region(event):
    cankeep = False
    while not(cankeep):
        #if
        #DBでevent.message.textを検索
        #あったら「地域を設定しました」と表示しreturn

        #一旦break
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
        print("while")
        break
    return "hello"