from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


app = Flask(__name__)
line_bot_api=LineBotApi('yc+KPHXOCoHuJSqYXTKs7kSoaipzx8MgBnbuB9Koh/UFnU8j6vddEXsqftChasIhYzWiKtIyNTGgs1gFwSQnoge6TUWfHyLEPZt1hP4cWapA6+IR50zN3/7og+rJ5MhmH3USfB6yIpI1o3pb43hS0QdB04t89/1O/w1cDnyilFU=')
handler=WebhookHandler('5aa5e458031f583b300e25e1164906d8')
line_bot_api.push_message('Ud7ccd071b5025d5a1d5006f4e620545f', TextSendMessage(text='你可以開始了'))

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
	     abort(400)
	return 'OK'
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

import os
if __name__ == "__main__":
     port=int(os.environ.get('PORT', 5000))
     app.run(host='0.0.0.0', port=port)
	
