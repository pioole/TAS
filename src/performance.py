import logging
import time


def perf(func):
    def wrapper(*args, **kwargs):
        beg_ts = time.time()
        retval = func(*args, **kwargs)
        end_ts = time.time()
        logging.debug('{} used {}s'.format(func.__name__, end_ts - beg_ts))
        return retval
    return wrapper
