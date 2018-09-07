# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 11:18:39 2018

@author: fuke masasi
"""

import tornado.ioloop
import tornado.web
import tornado.escape
import os, re
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
            ans = self.itr(sorted(list1, key=lambda k:k['no']))
        else:
            ans = self.itr(table.find().sort('no'))
        return ans
    
    def itr(self,item):
        i = 0
        ans = ''
        for x in item:
            ans += '*'+x['no']+'*  '
            if i == 2:
                ans += '\n'
                i = 0
            i += 1
        return ans
                        
    def post(self):
        '''
        signature = self.request.headers['X-Line-Signature']
        body = self.request.body
        parser = WebhookParser(ch)
        try:
            parser.parse(body, signature)
        except InvalidSignatureError:
            tornado.web.HTTPError(404)
            return
        '''
        dic = tornado.escape.json_decode(self.request.body)              
        for event in dic['events']:
            if 'replyToken' in event:
                linebot.reply_message(
                    event['replyToken'],
                    TextSendMessage(text=self.main(event['message']['text']))
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
    