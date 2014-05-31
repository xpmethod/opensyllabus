"""
Author: Maxim Kosinov
Specialization: Python, HighLoad Crawlers, Data Mining, Scraping
E-Mail: astrey.labs@gmail.com
Skype: geminiozz
O-Desk: Astrey
"""


DATA_DIR = '/mnt/osp-archive-mount/document-dump'
TMP_DIR = '/mnt/osp-archive-mount/document-dump/code/opensyllabus/_tmp'

# MongoDB configurations
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

PROCESS_REPORT_COUNT = 1000
THREAD_COUNT = 5

try:
    from opensyllabus.local_config import *
except ImportError:
    pass