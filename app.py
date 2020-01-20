# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import random
import time
from datetime import timedelta, datetime
from pymongo import MongoClient

#ref: http://twstock.readthedocs.io/zh_TW/latest/quickstart.html#id2
import twstock

import matplotlib
matplotlib.use('Agg') # ref: https://matplotlib.org/faq/howto_faq.html
import matplotlib.pyplot as plt
import pandas as pd

from imgurpython import ImgurClient

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)


channel_secret_8 = '5aa5e458031f583b300e25e1164906d8'
channel_access_token_8 = 'Hw+z4rxRO0Gp6BzOsELuUkpgaZrAs0CS+I9eJtY4/TRNhvw4c97D6JH77kchqLg0YzWiKtIyNTGgs1gFwSQnoge6TUWfHyLEPZt1hP4cWarA0LKPE8Ix03VUexECZimJPPmgHPaFV+FOB0Oxr8qYwQdB04t89/1O/w1cDnyilFU='
line_bot_api_8 = LineBotApi(channel_access_token_8)
parser_8 = WebhookParser(channel_secret_8)
line_bot_api_8.push_message('Ud7ccd071b5025d5a1d5006f4e620545f', TextSendMessage(text='你可以開始了'))

#===================================================
#   stock bot
#===================================================
#@app.route("/callback_yangbot8", methods=['POST'])
#def callback_yangbot8():
@app.route("/callback", methods=['POST'])
def callback():

    signature = request.headers['X-Line-Signature']

    # get request body as text
	#body = request.body.decode('utf-8')
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser_8.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
	
    #for event in events:
    #    if not isinstance(event, MessageEvent):
    #        continue
    #    if not isinstance(event.message, TextMessage):
    #        continue
	
	# 此處我們呼叫get_answer函數，從QnAMaker服務取得答案
		#answer = get_answer(event.message.text)
	#if isinstance(event, MessageEvent):
		#   line_bot_api_8.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
			
	line_bot_api_8.reply_message(event.reply_token,TextSendMessage(text=events))
	
    for event in events:
        if isinstance(event, MessageEvent):
            line_bot_api_8.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
        #if not isinstance(event.message, TextMessage):
        #    continue
		

        text=event.message.text
        #userId = event['source']['userId']
        if(text.lower()=='me'):
            content = str(event.source.user_id)

            line_bot_api_8.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
        elif(text.lower() == 'profile'):
            profile = line_bot_api_8.get_profile(event.source.user_id)
            my_status_message = profile.status_message
            if not my_status_message:
                my_status_message = '-'
            line_bot_api_8.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='Display name: ' + profile.display_name
                    ),
                    TextSendMessage(
                        text='picture url: ' + profile.picture_url
                    ),
                    TextSendMessage(
                        text='status_message: ' + my_status_message
                    ),
                ]
            )

        elif(text.startswith('#')):
            text = text[1:]
            content = ''

            stock_rt = twstock.realtime.get(text)
            my_datetime = datetime.fromtimestamp(stock_rt['timestamp']+8*60*60)
            my_time = my_datetime.strftime('%H:%M:%S')

            content += '%s (%s) %s\n' %(
                stock_rt['info']['name'],
                stock_rt['info']['code'],
                my_time)
            content += '現價: %s / 開盤: %s\n'%(
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

        elif(text.startswith('/')):
            text = text[1:]
            fn = '%s.png' %(text)
            stock = twstock.Stock(text)
            my_data = {'close':stock.close, 'date':stock.date, 'open':stock.open}
            df1 = pd.DataFrame.from_dict(my_data)

            df1.plot(x='date', y='close')
            plt.title('[%s]' %(stock.sid))
            plt.savefig(fn)
            plt.close()

            # -- upload
            # imgur with account: your.mail@gmail.com
            client_id = 'your imgur client_id'
            client_secret = 'your imgur client_secret'

            client = ImgurClient(client_id, client_secret)
            print("Uploading image... ")
            image = client.upload_from_path(fn, anon=True)
            print("Done")

            url = image['link']
            image_message = ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )

            line_bot_api_8.reply_message(
                event.reply_token,
                image_message
                )


    return 'OK'


@app.route("/", methods=['GET'])
def basic_url():
    return 'OK'


if __name__ == "__main__":
    app.run()
