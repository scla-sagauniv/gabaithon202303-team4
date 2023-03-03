from urllib import request
import json
from linebot.models import (
    TextSendMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction
)

from commons import *
from user import User
from location import Location
from exec_time import ExecTime

def get_location(uid):
    '''
    locationの指定をしてもらう関数

    Args:
        uid: string
    '''
    message = TextSendMessage(text='お住まいの都道府県を入力してね')
    line_bot_api.push_message(
            uid,
            messages=message
        )

def set_location(uid, message):
    user = User.fetch_info_by_uid(uid)
    location = Location.from_label(message)
    user.area_code = location.area_code
    user.update()


def set_exec_time(uid, message):
    user = User.fetch_info_by_uid(uid)
    if message in ExecTime().m_range:
        user.exec_time = message
    else:
        user.exec_time = f'{user.exec_time}:{message}'
    user.update()

def get_is_publick_send(uid):
    messages = TemplateSendMessage(
        alt_text='送られてくる画像はどっちがいい？',
        template=ConfirmTemplate(
          text='送られてくる画像はどっちがいい？',
          actions=[
              PostbackAction(
                  label='全てのペットたち',
                  display_text='全てのペットたち',
                  data=f'action={PostbackEventAction.SETUP.value}&uid={uid}&step={SetupStep.IS_PUBLIC_SEND.value}&value=1'
              ),
              PostbackAction(
                  label='自分のペットだけ',
                  display_text='自分のペットだけ',
                  data=f'action={PostbackEventAction.SETUP.value}&uid={uid}&step={SetupStep.IS_PUBLIC_SEND.value}&value=0'
              )
          ]
        )
    )
    line_bot_api.push_message(
            uid,
            messages=messages
        )

def set_is_publick_send(uid, value):
    user = User.fetch_info_by_uid(uid)
    user.is_public_send = value == '1' if True else False
    user.update()

def get_is_open_data(uid):
    messages = TemplateSendMessage(
        alt_text='登録した画像はみんなが見ていい？',
        template=ConfirmTemplate(
          text='登録した画像はみんなが見ていい？',
          actions=[
              PostbackAction(
                  label='全ユーザーへ公開',
                  display_text='全ユーザーへ公開',
                  data=f'action={PostbackEventAction.SETUP.value}&uid={uid}&step={SetupStep.IS_OPEN_DATA.value}&value=1'
              ),
              PostbackAction(
                  label='自分にだけ公開',
                  display_text='自分にだけ公開',
                  data=f'action={PostbackEventAction.SETUP.value}&uid={uid}&step={SetupStep.IS_OPEN_DATA.value}&value=0'
              )
          ]
        )
    )
    line_bot_api.push_message(
            uid,
            messages=messages
        )

def set_is_open_data(uid, value):
    user = User.fetch_info_by_uid(uid)
    user.is_open_data = value == '1' if True else False
    user.update()
    
def send_complete_message(uid):
    message = TextSendMessage(text='初期設定完了！！')
    line_bot_api.push_message(
            uid,
            messages=message
        )


def setup(uid, step, message=None):
    '''
    セットアップを行う関数
    stepで擬似的に状態管理を行う
    '''
    if step == SetupStep.CREATE.value:
        step = 0
        user = User(uid=uid)
        user.create()
        get_location(uid)
    elif step == SetupStep.LOCATION.value:
        set_location(uid, message)
        setup(uid, SetupStep.EXEC_TIME.value)
    elif step == SetupStep.EXEC_TIME.value:
        if message in ExecTime().merge_list():
            set_exec_time(uid, message)
        next_messages = ''
        if message in ExecTime().minute:
            get_is_publick_send(uid)
            return
        if message in ExecTime().hour:
            next_messages = create_quick_reply_message('何分？', ExecTime().minute)
        elif message in ExecTime().m_range:
            next_messages = create_quick_reply_message('何時？', ExecTime().hour)
        else: 
            line_bot_api.push_message(
                uid,
                messages=TextSendMessage(text='通知を送る時間を教えてね')
            )
            next_messages = create_quick_reply_message('時間帯は？', ExecTime().m_range)
        print(f'hoge;;{next_messages}')
        line_bot_api.push_message(
            uid,
            messages=next_messages
        )
    elif step == SetupStep.IS_PUBLIC_SEND.value:
        set_is_publick_send(uid, message)
        get_is_open_data(uid)
    elif step == SetupStep.IS_OPEN_DATA.value:
        set_is_open_data(uid, message)
        setup(uid, SetupStep.COMPLETE.value)
    elif step == SetupStep.COMPLETE.value:
        send_complete_message(uid)
        
            

