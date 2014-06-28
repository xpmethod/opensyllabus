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
from pymongo.errors import OperationFailure, AutoReconnect, DuplicateKeyError
from optparse import OptionParser, OptionGroup

# add project dir to PYTHONPATH
sys.path.insert(0, os.path.join(os.path.split(sys.path[0])[0]))

# so now we can import opensyllabus package
# from opensyllabus.core.extractor import DataExtractor
# from opensyllabus.core.mongo import OpenSyllabusDb
from opensyllabus.config import DATA_DIR, INGESTION_LOG_FILE, FILE_LOG_VERBOSITY, \
                                CONSOLE_LOG_VERBOSITY, THREADS_COUNT, LOG_TO_FILE
                                
from opensyllabus.core.ingestion import Ingester, StatCounter
from opensyllabus.core.utils import get_data_files, get_file_ext, configure_loggers, log_levels


log = logging.getLogger(__name__)


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
        options.log_file =  INGESTION_LOG_FILE
    
    if len(args) < 1:
        data_dir = DATA_DIR
    else:
        data_dir = args[1]
        
    log = configure_loggers(log,
                            log_levels[options.verbosity], 
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
 




