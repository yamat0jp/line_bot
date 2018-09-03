# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 11:18:39 2018

@author: fuke masasi
"""

import tornado.ioloop
import tornado.web
import tornado.escape
import json, os, hmac, base64, hashlib, pytz
from datetime import datetime
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


class WebHookHandler(tornado.web.RequestHandler):   
    def get(self):
        pz = pytz.timezone('Asia/Tokyo')
        t = datetime.now(pz).hour
        if (t >= 9)and(t < 16):
            self.write(u'仕事中.'+str(datetime.now()))
        else:
            self.write(str(t))
        
    def post(self):
        header = json.load(self.request.headers)
        body = json.load(self.request.body)
        hash = hmac.new(header['X-Line-Signature'].encode('utf-8'),
            body.encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(hash)
        '''
        try:
            events = webhook.parse(body, signature)
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
        '''
        self.write(header)
        
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