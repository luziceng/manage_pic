__author__ = 'cheng'
# -*- coding:utf-8 -*-
import logging
from tornado.options import options, define

class Logger():

    string_dict = {}

    def __init__(self, name="cafe"):
        cafe_logger = logging.getLogger(name)
        console = logging.StreamHandler()
        console.setLevel(logging.WARN)
        logging.getLogger().addHandler(console)
        self._logger = None
        if options.log_file_prefix:
            channel = logging.handlers.TimedRotatingFileHandler(
                filename = options.log_file_prefix,
                when = 'midnight',
                backupCount = options.log_file_num_backups
                )
            log_format = "[%(levelname)1.1s %(asctime)s %(name)s %(module)s:%(lineno)d] %(message)s"
            formatter = logging.Formatter(log_format)
            channel.setFormatter(formatter)
            cafe_logger.addHandler(channel)
            if options.dev:
                cafe_logger.setLevel(getattr(logging, 'DEBUG'))
            else:
                cafe_logger.setLevel(getattr(logging, 'INFO'))
            self._logger = cafe_logger


    def args2string(self, *args):
        l = len(args)
        _ = self.string_dict.get(l)
        if not _:
            _ = '%s ' * l
            self.string_dict[l] = _
        return _ % args

    def info(self, *args):
        if self._logger:
            self._logger.info(self.args2string(*args))
        else:
            print '-' * 10 + 'info' + '-' * 10
            print '%s ' * len(args) % args
            print '-' * 24


    def warn(self, *args):
        if self._logger:
            self._logger.warn(self.args2string(*args))
        else:
            print '-' * 10 + 'warn' + '-' * 10
            print '%s ' * len(args) % args
            print '-' * 24

    def debug(self, *args):
        if self._logger:
            self._logger.debug(self.args2string(*args))
        else:
            print '-' * 10 + 'debug' + '-' * 10
            print '%s ' * len(args) % args
            print '-' * 24

    def error(self, *args):
        if self._logger:
            self._logger.error(self.args2string(*args))
        else:
            print '-' * 10 + 'error' + '-' * 10
            print '%s ' * len(args) % args
            print '-' * 24


log = Logger()


class Entity(dict):
    def __getattr__(self, name, default = None):
        try:
            return self[name]
        except:
            return default

    def __setattr__(self, name, value = ""):
        self[name] = value



'''
size:每页条数
index:当前页码
rows:总条数
total:总页数
data:该页数据
next:是否有下一页
previous:是否有上一页
'''
class Page(Entity):
    def __init__(self, **kwargs):
        super(Page, self).__init__(kwargs)
        self['size'] = kwargs.get('size', options.count)
        self['index'] = kwargs.get('index', options.page)
        self['rows'] = kwargs.get('rows', 0)
        self['data'] = kwargs.get('data', [])

        self['total'] = (self['rows'] / self['size']) + (self['rows'] % self['size'] and 1 or 0)
        self['next'] = (self['index'] < self['total'])
        self['previous'] = (self['index'] > 1)

        self['limit'] = self['size']
        self['offset'] = (self['index'] - 1) * self['size']
