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

import os
import logging






class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            (r'/',IndexHandler),
            (r'/login',LoginHandler),
            (r'/register',RegistHandler),

        ]

        settings= dict(
            gzip = True,
            debug = False,
            template_path = os.path.join(os.path.dirname(__file__),"templates"),
            cookie_secret="luzicheng",
            static_path = os.path.join(os.path.dirname(__file__),"static"),
            xsrf_cookies=False,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    http_server =tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

