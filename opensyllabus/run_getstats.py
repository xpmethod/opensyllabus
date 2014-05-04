#!/usr/bin/env python
"""
Author: Maxim Kosinov
Specialization: Python, HighLoad Crawlers, Data Mining, Scraping
E-Mail: astrey.labs@gmail.com
Skype: geminiozz
O-Desk: Astrey
"""

import sys
from os.path import split as p_split, join

# add project dir to PYTHONPATH
sys.path.insert(0, join(p_split(sys.path[0])[0]))

# so now we can import opensyllabus package
from opensyllabus.config import DATA_DIR, PROCESS_REPORT_COUNT
from opensyllabus.core.exceptions import WrongFileExtension
from opensyllabus.core.utils import get_data_files, get_file_ext, get_file_dir


class ExtStats(object):
    
    def __init__(self):
        self.counter = 0
        self.ext_stats = {}
        self.valid_count = 0
        self.errors_count = 0
    
    def _show_stats(self):
        """
        Show calculated statistics
        """
        report = '\nExtensions Stats:\n' 
        for ext, count in self.ext_stats.iteritems():
            report += '%s: %s\n' % (ext, count)

        report += 'processed: %s\nvalid: %s\nerrors: %s' % (self.counter, self.valid_count, self.errors_count)
        print '=' * 80 + report + '=' * 80
        
    def _show_process_report(self, filepath):
        """
        Show statistics reports during file processing
        """
        self.counter += 1
        if self.counter % PROCESS_REPORT_COUNT == 0:
            print  'Processed (%s): %s files, errors: %s, stats: %s' % (get_file_dir(filepath), self.counter, self.errors_count, self.ext_stats)        
        
    def _calc_stats(self):
        """
        Calculating statistics for file extensions
        """
        for file in get_data_files():
            try:
                ext = get_file_ext(file)
            except WrongFileExtension:
                self.errors_count += 1
            else:
                self.valid_count += 1
                self.ext_stats[ext] = self.ext_stats.setdefault(ext, 0) + 1

            self._show_process_report(file)

    
    def run(self):
        """
        Main method for starting calculating
        """
        self._calc_stats()
        self._show_stats()
    

if __name__ == '__main__':
    ExtStats().run()
