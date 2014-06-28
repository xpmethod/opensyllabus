#!/usr/bin/env python
"""
Author: Maxim Kosinov
Specialization: Python, HighLoad Crawlers, Data Mining, Scraping
E-Mail: astrey.labs@gmail.com
Skype: geminiozz
O-Desk: Astrey
"""

import sys
import logging
from optparse import OptionParser, OptionGroup
from os.path import split as p_split, join, splitext

# add project dir to PYTHONPATH
sys.path.insert(0, join(p_split(sys.path[0])[0]))

# so now we can import opensyllabus package
from opensyllabus.core.mongo import OpenSyllabusDb
from opensyllabus.core.utils import configure_loggers, log_levels
from opensyllabus.config import GETEMPTY_LOG_FILE, FILE_LOG_VERBOSITY, CONSOLE_LOG_VERBOSITY, LOG_TO_FILE

log = logging.getLogger(__name__)


class BrokenDocsStats(object):
    
    def __init__(self, log):
        self.broken_ext_count = {}
        #--
        self.db = OpenSyllabusDb(log)


    def _get_broken_docs_1(self):
        """
        Get documents with empty 'text' field
        """
        for doc in self.db.get_empty_docs(''):
            ext = splitext(doc['filename'])[-1]
            self.broken_ext_count[ext] = self.broken_ext_count.setdefault(ext, 0) + 1
            print doc['path']


    def _get_broken_docs_2(self):
        """
        Get documents with null 'text' field
        """        
        for doc in self.db.get_empty_docs(None):
            ext = splitext(doc['filename'])[-1]
            self.broken_ext_count[ext] = self.broken_ext_count.setdefault(ext, 0) + 1
            print doc['path']
    
    def show_result(self):
        """
        Show calculated statistics
        """        
        report = '\nBroken Docs Stats:\n' 
        for ext, count in self.broken_ext_count.iteritems():
            report += '%s: %s\n' % (ext, count)
        print '=' * 80 + report + '=' * 80

    
    def get_broken_doc(self, doc_type):
        if doc_type == 'empty':
            self._get_broken_docs_1()
        else:
            self._get_broken_docs_2()
        #--
        self.show_result()


if __name__ == '__main__':
    parser = OptionParser(usage='Usage: %prog [options]')
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
        '-t', '--type', 
        dest='type',
        type='choice', 
        choices=('empty', 'null'), 
        help='setup broken doc type'
    )
    parser.add_option(
        '-l', '--log', 
        dest='log_file',        
        help='setup log file'
    )    


    options, args = parser.parse_args()
    
    if LOG_TO_FILE and not options.log_file:
        options.log_file =  GETEMPTY_LOG_FILE
        
    log = configure_loggers(log,
                            log_levels[options.verbosity], 
                            options.log_file,
                            log_levels[options.log_verbosity])    
    
    if not options.type:
        parser.error('-t option is mandatory')                
    else:
        BrokenDocsStats(log).get_broken_doc(options.type)

