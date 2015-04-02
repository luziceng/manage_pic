__author__ = 'cheng'
#!/usr/bin/env python
# _*_ coding: utf-8 _*_
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define ,options

define('application_name', default='manage apps picture', type = str)
define('port', default=9999, help='run on the given port', type=int)
define('page', default=1, type =int)
define('count', default=20, type=int)

# -*- coding:utf-8 -*-
import os
import logging


from control.login import  RegisterHandler,IndexHandler
from srvframe.base import  LoginHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            (r'/',IndexHandler),
            (r'/login',LoginHandler),
            (r'/register',RegisterHandler),
            (r'/upload', UploadHandler),
        ]

        settings= dict(
            gzip = True,
            debug = True,
            template_path = os.path.join(os.path.dirname(__file__),"templates"),
            cookie_secret="luzicheng",
            static_path = os.path.join(os.path.dirname(__file__),"static"),
            xsrf_cookies=False,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        def log_request(self, handler):
            if 'log_function' in self.settings:
                self.settings['log_function'](handler)
                return
            if handler.get_status() < 400:
                log_method = logging.info
            elif handler.get_status() < 500:
                log_method = logging.warning
            else:
                log_method = logging.error
            request_time = 1000.0 * handler.request.request_time()
            log_method('%d %s %.2fms queueSize:%d', handler.get_status(),
                handler._request_summary(), request_time,
                len(tornado.ioloop.IOLoop.instance()._events)+1)


class Logger():
    string_dict = {}
    def args2string(self, *args):
        l = len(args)
        _ = self.string_dict.get(l)
        if not _:
            _ = '%s ' * l
            self.string_dict[l] = _
        return _ % args
    def info(self, *args):
        logging.info(self.args2string(*args))
logger = Logger()



def main():
    tornado.options.parse_command_line()
    http_server =tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()