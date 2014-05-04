#!/usr/bin/env python
"""
Author: Maxim Kosinov
Specialization: Python, HighLoad Crawlers, Data Mining, Scraping
E-Mail: astrey.labs@gmail.com
Skype: geminiozz
O-Desk: Astrey
"""

import os
import sys

# add project dir to PYTHONPATH
sys.path.insert(0, os.path.join(os.path.split(sys.path[0])[0]))

# so now we can import opensyllabus package
from opensyllabus.core.utils import get_data_files, get_file_ext
from opensyllabus.core.extractor import DataExtractor
from opensyllabus.core.mongo import OpenSyllabusDb
from opensyllabus.config import PROCESS_REPORT_COUNT


class Extract(object):
    
    def __init__(self):
        self.counter = 0
        self.errors_count = 0
        self.success_count = 0
        self.ignored_count = 0
        self.wrang_ext_count = 0
        #--
        self.extractor = DataExtractor()
        self.os_db = OpenSyllabusDb()
        
    def _show_report(self):
        """
        Show extracting reort
        """ 
        report = '\nExtraction Stats:\nprocessed: %s\ninserted: %s\nignored: %s\nwrang ext: %s\nerrors: %s\n' % (self.counter, self.success_count, self.ignored_count, self.wrang_ext_count, self.errors_count)
        print '=' * 80 + report + '=' * 80
        
    def _show_process_report(self):
        """
        Show reports during file processing
        """
        self.counter += 1
        if self.counter % PROCESS_REPORT_COUNT == 0:
            print  'Processed (%s): inserted: %s, ignored: %s, wrang ext: %s, errors: %s' % (self.counter, self.success_count, self.ignored_count, self.wrang_ext_count, self.errors_count)        

    def _extract(self):
        for data_file in get_data_files():
            try:
                ext = get_file_ext(data_file)
            except:
                self.errors_count += 1
            else:
                if hasattr(self.extractor, ext):
                    if self.os_db.is_new(data_file):
                        try:
                            data = getattr(self.extractor, ext)(data_file)
                        except Exception as e:
                            self.errors_count += 1
                        else:
                            self.success_count += 1
                            try:
                                self.os_db.insert_data(data_file, os.path.split(data_file)[1], data)
                            except:
                                print data_file
                                raise
                    else:
                        self.ignored_count += 1
                else:
                    self.wrang_ext_count += 1
            #--
            self._show_process_report()

    def run(self):
        self._extract()
        self._show_report()

                

if __name__ == '__main__':
    Extract().run()
