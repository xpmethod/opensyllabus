# -*- coding:utf8 -*-
"""
Author: Maxim Kosinov
Specialization: Python, HighLoad Crawlers, Data Mining, Scraping
E-Mail: astrey.labs@gmail.com
Skype: geminiozz
O-Desk: Astrey
"""


DATA_DIR = '/mnt/osp-archive-mount/document-dump'
TMP_DIR = '/mnt/osp-archive-mount/document-dump/code/opensyllabus/_tmp'

# log config
LOG_TO_FILE = True
FILE_LOG_VERBOSITY = 'debug'
CONSOLE_LOG_VERBOSITY = 'debug'
INGESTION_LOG_FILE = '/mnt/osp-archive-mount/document-dump/code/opensyllabus/_logs/ingestion.log'
GETEMPTY_LOG_FILE = '/mnt/osp-archive-mount/document-dump/code/opensyllabus/_logs/get_empty.log'

# MongoDB configurations
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_USE_AUTH = True
MONGODB_USER = 'script'
MONGODB_PASSWORD = 'c*;,(yHfmz4J&Ap'

PROCESS_REPORT_COUNT = 500
THREADS_COUNT = 10

try:
    from opensyllabus.local_config import *
except ImportError:
    pass