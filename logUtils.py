import logging

def getLogger():
    logger = logging.getLogger('big_project')
    hdlr = logging.FileHandler('logs/web.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)
    return logger