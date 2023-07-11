import datetime
import logging as logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import os
import time


def get_datetime_now():
    dt_now = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    return dt_now


PATH_THIS_FILE = os.path.realpath(__file__)
PATH_PARENT = os.path.abspath(os.path.dirname(__file__))
PATH_PARENT_PARENT = os.path.abspath(os.path.join(PATH_PARENT, os.pardir))
PATH_LOGS = os.path.join(PATH_PARENT_PARENT, 'logs', 'script.log')




logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(u'%(asctime)s\t%(levelname)s\t%(filename)s:%(lineno)d\t%(message)s')


# create TimedRotatingFileHandler
# rotation_logging_handler = TimedRotatingFileHandler(PATH_LOGS,
#                                when='m',
#                                interval=1,
#                                backupCount=5)
# rotation_logging_handler.setLevel(logging.DEBUG)
# rotation_logging_handler.setFormatter(formatter)
# logger.addHandler(rotation_logging_handler)


# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


# Create a file handler
# fh = logging.FileHandler(PATH_LOGS)
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(formatter)
# logger.addHandler(fh)


# Create RotatingFileHandler
rfh = RotatingFileHandler(PATH_LOGS, maxBytes=100_000, backupCount=10)
rfh.setLevel(logging.DEBUG)
rfh.setFormatter(formatter)
logger.addHandler(rfh)


# if __name__ == '__main__':
#     import pandas as pd
#
#     new_my_dict = [
#         {'a': 15, 'n': 81, 'p': 177},
#         {'a': 18, 'n': 24, 'c':22, 'p': 190},
#         {'a': 19, 'n': 20, 'p': 156},
#     ]
#
#     df = pd.DataFrame.from_dict(new_my_dict)
#     print(df)
#     # df.to_csv(r'test8.csv', index=False, header=True)
