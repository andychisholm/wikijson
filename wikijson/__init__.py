import logging

logFormat = '%(asctime)s|%(levelname)s|%(module)s|%(message)s'
logging.basicConfig(format=logFormat)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
