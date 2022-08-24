import os
import re
import datetime
import logging

class Logger():
    def __init__(self, szLogPrefixName):
        # Log Path
        self.szLogPath = os.getcwd() + "\\logs\\"

        # Create Logs Dirpath
        if not os.path.exists(self.szLogPath):
            os.makedirs(self.szLogPath)

        # Log File Name
        self.szLogPrefixName = szLogPrefixName
        self.szLogSuffixName = "%Y-%m-%d.log"
        self.szLogFileNameFmt = os.path.join(self.szLogPath, self.szLogPrefixName + "_" + self.szLogSuffixName)
        self.szLogFile = datetime.datetime.now().strftime(self.szLogFileNameFmt)
        
        self.formattler = "%(asctime)s [%(levelname)-8s] %(message)s"
        self.logger = logging.basicConfig(level=logging.DEBUG, filename=self.szLogFile, filemode='a+',
                                          datefmt='%Y/%m/%d %H:%M:%S', format=self.formattler)
    
    def debug(self, szMsg):
        print(szMsg)
        logging.debug(szMsg)

    def info(self, szMsg):
        print(szMsg)
        logging.info(szMsg)

    def warning(self, szMsg):
        print(szMsg)
        logging.warning(szMsg)

    def error(self, szMsg):
        print(szMsg)
        logging.error(szMsg)

    def critical(self, szMsg):
        print(szMsg)
        logging.critical(szMsg)

        







