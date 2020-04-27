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

app = Flask(__name__)

line_bot_api = LineBotApi('g2OY4/RRBTq8GrRWZvoR5qoELk5prTPueeuh21W4zGlHFqQBYUMb3wtBouvSc9Sr3kOYrQX2DGmlZJFLdm++1J1YLgFF7dAptJglLFkGmzabgvlfVpfjMv/HS9MZwAale5bxsjP9+hBGslGJoUsXAAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('79e3f52ef938a4a98c8974432fac3bed')


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
    msg = event.message.text
    r = '很抱歉，您说什么'

    if msg in ['hi', 'Hi']:
        r = 'hi'
    elif msg == '你吃饭了吗':
        r = '还没'
    elif msg == '你是谁':
        r = '我是机器人'
    elif '订位' in msg:
        r = '您想订位，是吗？'
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id='1',
            sticker_id='1'
    ))


if __name__ == "__main__":
    app.run()