# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 11:18:39 2018

@author: fuke masasi
"""

import tornado.ioloop
import tornado.web
import json, os, hmac, base64, hashlib
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


class WebHookHandler(tornado.web.RequestHandler):    
    def post(self):
        header = json.load(self.request.headers['X-Line-Signature'])
        body = json.load(self.request.body)
        hash = hmac.new(header.encode('utf-8'),
            body.encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(hash)
        events = webhook.parse(body, signature)
        '''
        try:
            events = webhook.parse(body, signature)
        except InvalidSignatureError:
            raise tornado.web.HTTPError(400)
            return
        '''
        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessage):
                continue
            linebot.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )
        
class DummyHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('OK')

application = tornado.web.Application([(r'/callback',WebHookHandler),(r'/',DummyHandler)])

if __name__ == '__main__':
    token = os.environ['Access_Token']
    ch = os.environ['Channel_Secret']
    linebot = LineBotApi(token)
    webhook = WebhookParser(ch)  
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()