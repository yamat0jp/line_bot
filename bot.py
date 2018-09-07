# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 11:18:39 2018

@author: fuke masasi
"""

import tornado.ioloop
import tornado.web
import tornado.escape
import os, hmac, base64, hashlib, re
import pytz, pymongo
from datetime import datetime
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage


class WebHookHandler(tornado.web.RequestHandler):   
    def get(self):
        mes = self.get_argument('code','')
        self.write(self.main(mes))
        
    def main(self,no):
        pz = pytz.timezone('Asia/Tokyo')
        now = datetime.now(pz)
        t = now.hour
        w = now.weekday()
        if (w < 5)and(t >= 9)and(t < 16):
            return u'仕事中.'
        db = pymongo.MongoClient(uri)[ac]
        table = db['glove']
        item = table.find({'no':re.compile(no,re.IGNORECASE)})
        if item.count() == 1:
            x = item[0]
            ans = x['name']+'\n'+x['no']
        elif item.count() > 1:
            ans = ''    
            obj = list(item)
            list1 = sorted(obj, key=lambda k:k['name'])
            for x in list1:
                if x['name'] == list1[0]['name']:
                    ans += x['name']+'\n'+x['no']+'\n'
                else:
                    break
            else:
                return ans         
            ans = ''             
            for x in sorted(list1, key=lambda k:k['no']):
                ans += x['no']+'\n'
        else:
            ans = ''
            for x in table.find().sort('no'):
                ans += x['no']+'\n'
        return ans
            
    def post(self):
        header = self.request.headers
        body = self.request.body.decode('utf-8')
        '''
        hashid = hmac.new(header.get('X-Line-Signature'),
            body.decode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(hashid)
        '''
        parser = WebhookParser(ch)
        try:
            events = parser.parse(body, header)
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

application = tornado.web.Application([(r'/callback',WebHookHandler),(r'/init',DummyHandler)])

if __name__ == '__main__':
    token = os.environ['Access_Token']
    ch = os.environ['Channel_Secret']
    uri = os.environ['MONGODB_URI']
    ac = os.environ['ACCOUNT']
    port = int(os.environ.get('PORT',5000))#important in heroku
    linebot = LineBotApi(token)
    webhook = WebhookParser(ch)  
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
    