# @Author: chenrw
# -*- coding:utf-8 -*-
# @Time: 2020-4-2 19:28
# @File: base_logging.py
import logging
from common_data.dir_path import *


class Log:
    def __init__(self, name=None):
        is_exist = os.path.exists(LogPath)
        if not is_exist:
            os.makedirs(LogPath)
        # self.log_name = os.path.join(LogPath, '%s.log' % time.strftime('%m_%d_%H'))
        self.log_name = os.path.join(LogPath, '{}.log'.format(time.strftime('%m_%d_%H_%M_%S')))
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('[%(asctime)s] -%(name)s - %(levelname)s:  %(message)s')

    def __console(self, level, message):
        # 创建一个FileHandler,用于写到本地
        fh = logging.FileHandler(self.log_name, 'a', encoding="utf-8")
        fh.setLevel(logging.INFO)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)
        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)
        if level == "info":
            self.logger.info(message)
        elif level == "debug":
            self.logger.debug(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        fh.close()
        ch.close()
    def debug(self, message):
        self.__console("debug", message)

    def info(self, message):
        self.__console("info", message)

    def warning(self, message):
        self.__console("warning", message)

    def error(self, message):
        self.__console("error", message)



if __name__ == '__main__':
    log = Log("tesstNG")
    log.info("开始")
    log.warning("结束")



