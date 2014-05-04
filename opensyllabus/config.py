"""
Author: Maxim Kosinov
Specialization: Python, HighLoad Crawlers, Data Mining, Scraping
E-Mail: astrey.labs@gmail.com
Skype: geminiozz
O-Desk: Astrey
"""


#DATA_DIR = '/home/qnx/My Work/projects/opensyllabus/'
#DATA_DIR = '/mnt/osp-archive-mount/document-dump/leipzig'
#DATA_DIR = '/mnt/osp-archive-mount/document-dump/mikes-collection'
# DATA_DIR = '/mnt/osp-archive-mount/document-dump/lindas-corpus'
#DATA_DIR = '/mnt/osp-archive-mount/document-dump/cohen-archive'
DATA_DIR = '/mnt/osp-archive-mount/document-dump'

# MongoDB configurations
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

PROCESS_REPORT_COUNT = 20000

try:
    from opensyllabus.local_config import *
except ImportError:
    pass