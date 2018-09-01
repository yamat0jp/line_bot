# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 11:18:39 2018

@author: fuke masasi
"""

import tornado.ioloop
import tornado.web
import json, os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


class WebHookHandler(tornado.web.RequestHandler):    
    def post(self):
        signature = json.load(self.request.headers['X-Line-Signature'])
        data = json.load(self.request.body)
        try:
            events = webhook.handle(data, signature)
        except InvalidSignatureError:
            raise tornado.web.HTTPError(400)
            return
        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessage):
                continue
            linebot.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )
        self.set_status(200)

application = tornado.web.Application([(r'/callback',WebHookHandler)])

if __name__ == '__main__':
    token = os.environ['Channel_ID']
    ch = os.environ['Channel_Secret']
    linebot = LineBotApi(token)
    webhook = WebhookHandler(ch)  
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()