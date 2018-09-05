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
from linebot.models import TextSendMessage


class WebHookHandler(tornado.web.RequestHandler):   
    def get(self):
        self.write(self.main('2'))
        
    def main(self,no):
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
        item = table.find({'no':re.compile(no)})
        if item.count() == 1:
            ans = item['name']+'\n'+item['no']
        else:
            ans = ''
            for x in item.sort('no'):
                ans += x['no']+'\n'
            if ans == '':
                for x in table.find().sort('no'):
                    ans += x['no']+'\n'
        return ans
        
    def post(self):
        header = json.load(self.request.headers)
        body = json.load(self.request.body)
        hash = hmac.new(header['X-LINE-SIGNATURE'].encode('utf-8'),
            body.encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(hash)
        try:
            events = webhook.parse(body, signature)
        except InvalidSignatureError:
            raise tornado.web.HTTPError(400)
            return
        for event in events:
            if (event['type'] == 'text')and(event['message']['type'] == 'text'):
                linebot.reply_message(
                    event.reply_token,
                    TextSendMessage(text=self.main(event.Message.text))
                )
        
class DummyHandler(tornado.web.RequestHandler):
    def get(self):
        f = open('data.txt')
        data = f.read()
        f.close()
        db = pymongo.MongoClient(uri)[ac]
        table = db['glove']
        item = []
        for x in data.split('\n'):
            if x[0] == '@':
                dic = {}
                dic['name'] = x[1:]
            else:
                dic['no'] = x
                item.append(dic)
        table.remove()
        for x in item:
            table.insert(x)

application = tornado.web.Application([(r'/callback',WebHookHandler),(r'/init',DummyHandler)],{'Debug':True})

if __name__ == '__main__':
    token = os.environ['Access_Token']
    ch = os.environ['Channel_Secret']
    uri = os.environ['MONGODB_URI']
    ac = os.environ['ACCOUNT']
    linebot = LineBotApi(token)
    webhook = WebhookParser(ch)  
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
    