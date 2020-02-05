from __future__ import unicode_literals
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *


app = Flask(__name__)
line_bot_api=LineBotApi('Hw+z4rxRO0Gp6BzOsELuUkpgaZrAs0CS+I9eJtY4/TRNhvw4c97D6JH77kchqLg0YzWiKtIyNTGgs1gFwSQnoge6TUWfHyLEPZt1hP4cWarA0LKPE8Ix03VUexECZimJPPmgHPaFV+FOB0Oxr8qYwQdB04t89/1O/w1cDnyilFU=')
handler=WebhookHandler('5aa5e458031f583b300e25e1164906d8')
line_bot_api.push_message('Ud7ccd071b5025d5a1d5006f4e620545f', TextSendMessage(text='你可以開始了'))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
	signature=request.headers['X-Line-Signature']
	# get request body as text
	body=request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	# handle webhook body
	try:
	     handler.handle(body, signature)
	except InvalidSignatureError:
	     abort(400)
	return 'OK'
	
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	print(event)
	text=event.message.text
	if (text=="Hi"):
	    reply_text = "Hello John"
		#Your user ID
	elif(text=="你好"):
	    reply_text = "哈囉"
	elif(text=="機器人"):
	    reply_text = "叫我嗎"
	elif(text.startswith('#')):
	    text=text[1:]
	    #content='    '
	    stock_rt=twstock.realtime.get(text)
	    my_datetime = datetime.fromtimestamp(stock_rt['timestamp']+8*60*60)
	    my_time = my_datetime.strftime('%H:%M:%S')
	    content += '%s (%s) %s\n' %(
            stock_rt['info']['name'],
            stock_rt['info']['code'],
            my_time)
            content+='現價: %s / 開盤: %s\n'%(
            stock_rt['realtime']['latest_trade_price'],
            stock_rt['realtime']['open'])
            content += '最高: %s / 最低: %s\n' %(
            stock_rt['realtime']['high'],
            stock_rt['realtime']['low'])
            content += '量: %s\n' %(stock_rt['realtime']['accumulate_trade_volume'])
            stock = twstock.Stock(text)#twstock.Stock('2330')
            content += '-----\n'
            content += '最近五日價格: \n'
            price5 = stock.price[-5:][::-1]
            date5 = stock.date[-5:][::-1]
            for i in range(len(price5)):
                #content += '[%s] %s\n' %(date5[i].strftime("%Y-%m-%d %H:%M:%S"), price5[i])
                content += '[%s] %s\n' %(date5[i].strftime("%Y-%m-%d"), price5[i])
                line_bot_api_8.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
                )
	else:
	    reply_text = text
	#message=TextSendMessage(text=event.message.text)
	message=TextSendMessage(reply_text)
	line_bot_api.reply_message(event.reply_token,message)
	
import os
if __name__ == "__main__":
     port=int(os.environ.get('PORT', 3000))
     app.run(host='0.0.0.0', port=port)
	
