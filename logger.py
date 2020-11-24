import os
import sys
import logging
import constants


def setup_logger(name):
    logname = str(name)
    logfile = os.path.join(constants.LOG_FOLDER, constants.LOG_NAME_FORMAT.format(name))

    os.makedirs(constants.LOG_FOLDER, exist_ok=True)

    logr = logging.getLogger(logname)
    logr.setLevel(logging.INFO)

    if len(logr.handlers) > 0:
        return logr

    logf = logging.FileHandler(logfile)
    logf.setFormatter(logging.Formatter(constants.LOG_FORMAT))
    logf.setLevel(logging.INFO)
    logr.addHandler(logf)

    logc = logging.StreamHandler(sys.stdout)
    logc.setFormatter(logging.Formatter(constants.LOG_FORMAT))
    logc.setLevel(logging.INFO)
    logr.addHandler(logc)

    return logr


def clean_log(name):
    logfile = os.path.join(constants.LOG_FOLDER, constants.LOG_NAME_FORMAT.format(name))
    try:
        os.unlink(logfile)
    except FileNotFoundError:
        pass