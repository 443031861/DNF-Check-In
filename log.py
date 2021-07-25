import logging
from colorama import Fore,Style
import sys
import colorlog
import time

# 获取对象
def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
 
    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            " %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger
 
#通过静态成员方法来调用
class Log:
 
    logger = get_logger()

    @staticmethod
    def getTime():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    @staticmethod
    def title(msg):
        Log.logger.info(Fore.YELLOW + "[当前节点]:  " +  str(msg)  + Style.RESET_ALL)

    @staticmethod
    def node(msg):
        Log.logger.info(Fore.LIGHTBLUE_EX + "[NODE "+ str(Log.getTime()) +" ]: " + str(msg) + Style.RESET_ALL)

    @staticmethod
    def hint(msg):
        Log.logger.info(Fore.RED + "[INFO "+ str(Log.getTime()) +" ]: " + str(msg) + Style.RESET_ALL)

    @staticmethod
    def debug(msg):
        Log.logger.debug(Fore.WHITE + "[DEBUG]: " + str(msg) + Style.RESET_ALL)
 
    @staticmethod
    def info(msg):
        Log.logger.info(Fore.GREEN + "[INFO "+ str(Log.getTime()) +" ]: " + str(msg) + Style.RESET_ALL)
 
    @staticmethod
    def warning(msg):
        Log.logger.warning("\033[38;5;214m" + "[WARNING]: " + str(msg) + "\033[m")
 
    @staticmethod
    def error(msg):
        Log.logger.error(Fore.RED + "[ERROR]: " + str(msg) + Style.RESET_ALL)
 
    @staticmethod
    def critical(msg):
        Log.logger.critical(Fore.RED + "[CRITICAL]: " + str(msg) + Style.RESET_ALL)