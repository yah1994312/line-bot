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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()