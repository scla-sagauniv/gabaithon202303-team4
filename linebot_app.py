import config   # 先ほど作成したconfig.pyをインポート
from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import weather
 
app = Flask(__name__)
 
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)    # config.pyで設定したチャネルアクセストークン
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)    # config.pyで設定したチャネルシークレット
 
 
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
 
    # get request body as text
    body = request.get_data(as_text=True)
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
    if event.reply_token == "00000000000000000000000000000000":
        return
 
    message = f"今日の天気は{weather.weather_label}。\n今日の降水確率は6時間ごとに、\n{weather.rainpc}(％)。\n今日の最高気温は、{weather.maxtemp}。\n今日の最低気温は、{weather.mintemp}。"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(message)
          )
 
if __name__ == "__main__":
    app.run(host="localhost", port=8000)   # ポート番号を8000に指定