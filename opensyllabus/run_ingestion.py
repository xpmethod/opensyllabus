#!/usr/bin/env python
"""
Author: Maxim Kosinov
Specialization: Python, HighLoad Crawlers, Data Mining, Scraping
E-Mail: astrey.labs@gmail.com
Skype: geminiozz
O-Desk: Astrey
"""

import os
import re
import sys
import time
import Queue
import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler, FileHandler, Formatter
from pymongo.errors import OperationFailure, AutoReconnect, DuplicateKeyError
from optparse import OptionParser, OptionGroup

# add project dir to PYTHONPATH
sys.path.insert(0, os.path.join(os.path.split(sys.path[0])[0]))

# so now we can import opensyllabus package
# from opensyllabus.core.extractor import DataExtractor
# from opensyllabus.core.mongo import OpenSyllabusDb
from opensyllabus.config import DATA_DIR, LOG_FILE, FILE_LOG_VERBOSITY, \
                                CONSOLE_LOG_VERBOSITY, THREADS_COUNT, LOG_TO_FILE
                                
from opensyllabus.core.ingestion import Ingester, StatCounter
from opensyllabus.core.utils import get_data_files, get_file_ext

log = logging.getLogger(__name__)
log_levels = {
    'debug': logging.DEBUG, 
    'info': logging.INFO, 
    'warning': logging.WARNING, 
    'error': logging.ERROR
}


def configure_loggers(verbosity, log_file, log_verbosity):
    LOGFMT_CONSOLE = ('[%(asctime)s] %(name)-10s %(levelname)-7s in %(module)s.%(funcName)s(),'
                      ' line %(lineno)d\n\t%(message)s')
    
    LOGFMT_FILE = ('[%(asctime)s] [%(process)d]%(name)-10s %(levelname)-7s in %(module)s.%(funcName)s(),'
                   ' line %(lineno)d\n\t%(message)s')

    # Configure root logger to log to stdout
    logging.basicConfig(level=verbosity, datefmt='%H:%M:%S', format=LOGFMT_CONSOLE)
    
    # Configure main logger to rotate log files
    rh = RotatingFileHandler(log_file, maxBytes=2000000, backupCount=25)
    log.addHandler(rh)

    # Configure main logger to log to a file
    if log_file:
        fh = FileHandler(log_file, 'w')
        fh.setFormatter(Formatter(LOGFMT_FILE, '%Y-%m-%d %H:%M:%S'))
        fh.setLevel(log_verbosity)
        log.addHandler(fh)


if __name__ == '__main__':
    
    parser = OptionParser(usage='Usage: %prog [options] dir')
    parser.add_option(
        '-v', '--verbosity', 
        dest='verbosity',
        type='choice', 
        choices=log_levels.keys(), 
        default=CONSOLE_LOG_VERBOSITY,
        help='setup console log verbosity'
    )

    parser.add_option(
        '-f', '--log-verbosity', 
        dest='log_verbosity',
        type='choice', 
        choices=log_levels.keys(), 
        default=FILE_LOG_VERBOSITY,
        help='setup file log verbosity'
    )

    parser.add_option(
        '-t', '--threads_count', 
        dest='threads_count',
        default=THREADS_COUNT,        
        help='setup threads count'
    )

    parser.add_option(
        '-l', '--log', 
        dest='log_file',        
        help='setup log file'
    )

    options, args = parser.parse_args()
    
    if LOG_TO_FILE and not options.log_file:
        options.log_file =  LOG_FILE
    
    if len(args) < 1:
        data_dir = DATA_DIR
    else:
        data_dir = args[1]
        
    configure_loggers(log_levels[options.verbosity], 
                      options.log_file,
                      log_levels[options.log_verbosity])
    
    log.info('Ingestion started: %s' % data_dir)
    
    queue = Queue.Queue()
    counter = StatCounter()

    for i in range(options.threads_count):
        ingester = Ingester(queue, log, counter)
        ingester.setDaemon(True)
        ingester.start()
        
    for data_file in get_data_files():
        queue.put(data_file)
        
    queue.join()
    
    counter.show_report()
 




