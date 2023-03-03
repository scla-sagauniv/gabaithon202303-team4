from linebot.models import (
    TextSendMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction
)

from commons import *    

def create_postback_quick_reply(uid, uuid, text, labels):
    '''
    画像をラベリングするためのクイックリプライを作る関数

    Args:
        uid: string
        uuid: string
        text: string
        labels: ImageLabelCategoryのvalue
    Respons: TextSendMessage
    '''
    quick_reply_buttons = []
    for label in labels:
        action = PostbackAction(
            label=label.value['label'], 
            display_text=label.value['display_label'], 
            data=f'action={PostbackEventAction.LABELING.value}&uid={uid}&uuid={uuid}&category={ImageLabelCategory(labels)}&value={label.value}'
        )
        quick_reply_buttons.append(QuickReplyButton(action=action))
    messages = TextSendMessage(text=text,
                               quick_reply=QuickReply(items=quick_reply_buttons))
    return messages
    

def get_img_labeling(uid, uuid, category):
    '''
    画像にラベル付けをするメッセージのプロバイダー

    Args:
        uid: string
        uuid: string
        category: ImageLabelCategory
    '''
    text = category == ImageLabelCategory.WEATHER if 'この画像の天気はズバリ何？' else 'じゃー、気温は暑い？寒い？それとも常温？'
    messages = create_postback_quick_reply(uid, uuid, text, category.value)
    line_bot_api.push_message(
        uid,
        messages=messages
    )

def set_img_labeling(uuid, labels):
    setter(uuid, labels)
    