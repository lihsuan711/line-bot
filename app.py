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

line_bot_api = LineBotApi('NucXwfzSqA+z7AWdjfWWsdfqoPkEIqBbwgsoZsenJWFDt5ZDFoM7ueXH+UloR+sg9razpYbf++wNGufwq1EAa7hBcOeW++3H107tiTRr9AjnLdBFagF0VzJ4Y1atFOKLb4eh+s1CfwHsYwQ0VA6dCAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b4c942bd7590cec7f06df5c1324abdf4')


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