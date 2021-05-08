import logging

class mylogger:

    def __init__(self, loggername):
        self.loggername = loggername

    def createLogger(self):
        logger = logging.getLogger(self.loggername)
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(filename = '/home/ec2-user/pip/mysite/all-logs', encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(name)s : %(levelname)s : %(asctime)s : %(message)s')

        fh.setFormatter(formatter)

        logger.addHandler(fh)
        return logger
