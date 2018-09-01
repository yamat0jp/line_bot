# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 11:18:39 2018

@author: fuke masasi
"""

import tornado.ioloop
import tornado.web
import json


verify_token = <VERIFY_TOKEN>

class WebhookHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('hub.verify_token','')
        if token == verify_token:
            write(token)
        else:
            write('Error, wrong varidation Token.)

application = tornado.web.Application([(r'webhook',WebHookHandler)])

if __name__ == '__main__':
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()