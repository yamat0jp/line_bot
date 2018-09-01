# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 11:18:39 2018

@author: fuke masasi
"""

import tornado.ioloop
import tornado.web
import json, os


class WebHookHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('hub.verify_token','')
        if token == ch:
            write(token)
        else:
            write('Error, wrong varidation Token.')

application = tornado.web.Application([(r'/callback',WebHookHandler)],{
        'debug':True
        })

if __name__ == '__main__':
    ch_ic = os.environ['Channel_ID']
    ch = os.environ['Channel_Secret']
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()