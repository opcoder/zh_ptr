#encoding:utf8
import logging
import logging.handlers
from logging import *
from datetime import *

logger = logging.getLogger('ptr')
logger.setLevel(logging.DEBUG)

# rht = logging.handlers.TimedRotatingFileHandler("reindex_out.log", 'D')
rht = logging.StreamHandler()
fmt = logging.Formatter("%(asctime)s %(filename)s:%(lineno)s@%(funcName)s", "%Y-%m-%d %H:%M:%S")
rht.setFormatter(fmt)
logger.addHandler(rht)

debug = logger.debug
info = logger.info
warning = logger.warn
error = logger.error
critical = logger.critical