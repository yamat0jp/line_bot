# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 11:18:39 2018

@author: fuke masasi
"""

import tornado.ioloop
import tornado.web
import tornado.escape
import json, os, hmac, base64, hashlib, pytz, pymongo, re
from datetime import datetime
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


class WebHookHandler(tornado.web.RequestHandler):   
    def get(self):
        pz = pytz.timezone('Asia/Tokyo')
        now = datetime.now(pz)
        t = now.hour
        w = now.weekday()
        if (w < 5)and(t >= 9)and(t < 16):
            obj = {'type':'text','text':u'仕事中'}
            j = json.dump(obj, ensure_ascii=False)
            self.write(j)
            return
        db = pymongo.MongoClient(uri)[ac]
        table = db['glove']
        if table.find().count() == 0: 
            table.insert_one({'name':u'リフレフィット','no':'SF'})
        no = 'SF'
        item = table.find({'no':no})
        if item.count() == 1:
            dic = {item['name']:item['no']}
        elif item.count() == 0:
            dic = {}
            for x in list(item.sort('no')):
                dic[x['name']] = x['no']
        else:
            item = table.find({'no':re.compile(no)})
            dic = {}
            for x in list(item.sort('no')):
                dic[x.name] = x['no']
        self.write(dic)
        
    def post(self):
        header = json.load(self.request.headers)
        body = json.load(self.request.body)
        hash = hmac.new(header['X-LINE-SIGNATURE'].encode('utf-8'),
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
    uri = os.environ['MONGODB_URI']
    ac = os.environ['ACCOUNT']
    linebot = LineBotApi(token)
    webhook = WebhookParser(ch)  
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()