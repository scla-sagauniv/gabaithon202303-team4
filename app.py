import flask
from flask import Flask, request, abort, render_template

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    PostbackEvent, FollowEvent, MessageEvent, TextMessage, TextSendMessage,
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

if __name__ == "__main__":
    app.run()
