# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 11:18:39 2018

@author: fuke masasi
"""

import tornado.ioloop
import tornado.web
import json, os
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


class WebHookHandler(tornado.web.RequestHandler):
    def post(self):
        global webhook
        signature = json.load(self.request.headers['X-Line-Signature'])
        data = json.load(self.request.body)
        try:
            events = webhook.parse(data, signature)
        except InvalidSignatureError:
            abort(400)
        for event in events:
            if not isinstance(event,MessageEvent):
                continue
            if not isinstance(event.message,TextMessage):
                continue
            linebot.reply_message(
                event.rply_token,
                TextSendMessage(text=event.message.text)
            )
        return 'OK'

application = tornado.web.Application([(r'/callback',WebHookHandler)],{
        'debug':True
        })

if __name__ == '__main__':
    ch_id = os.environ['Channel_ID']
    ch = os.environ['Channel_Secret']
    linebot = LineBotApi(ch_id)
    Webhook = WebhookParser(ch)  
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()