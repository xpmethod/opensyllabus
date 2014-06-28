# -*- coding:utf8 -*-
"""
Author: Maxim Kosinov
Specialization: Python, HighLoad Crawlers, Data Mining, Scraping
E-Mail: astrey.labs@gmail.com
Skype: geminiozz
O-Desk: Astrey
"""

import os
import sys
import threading
from time import time

# add project dir to PYTHONPATH
#sys.path.insert(0, os.path.join(os.path.split(sys.path[0])[0]))

# so now we can import opensyllabus package
from opensyllabus.core.mongo import OpenSyllabusDb
from opensyllabus.core.extractor import TextExtractor
from opensyllabus.config import PROCESS_REPORT_COUNT
from opensyllabus.core.utils import get_data_files, get_file_ext, get_file_type


class StatCounter(object):
    
    def __init__(self):
        self.processed = 0
        self.ingested = 0
        self.unsupported = 0
        self.wrong = 0
        self.ignored = 0
        #--
        self.proc_lock = threading.Lock()
        self.ing_lock = threading.Lock()
        self.unsupp_lock = threading.Lock()
        self.wrong_lock = threading.Lock()
        self.ignore_lock = threading.Lock()
        #--
        self.report_lock = threading.Lock()
        #--
        self.time = time()
        
    def inc_proc(self):
        self.proc_lock.acquire()
        try:
            self.processed += 1
            if self.processed % PROCESS_REPORT_COUNT == 0:
                self.show_process_report()
        finally:
            self.proc_lock.release()

    def inc_ing(self):
        self.ing_lock.acquire()
        try:
            self.ingested += 1
        finally:
            self.ing_lock.release()


    def inc_unsupp(self):
        self.unsupp_lock.acquire()
        try:
            self.unsupported += 1
        finally:
            self.unsupp_lock.release()

    def inc_wrong(self):
        self.wrong_lock.acquire()
        try:
            self.wrong += 1
        finally:
            self.wrong_lock.release()

    def inc_ignore(self):
        self.ignore_lock.acquire()
        try:
            self.ignored += 1
        finally:
            self.ignore_lock.release()

    def show_report(self):
        """
        Show summary report
        Input: None
        Output: None
        """ 
        report = '\nIngestion Stats:\n'
        report += 'processed: %s\n' % self.processed
        report += 'ingested: %s\n' % self.ingested
        report += 'unsupported ext: %s\n' % self.unsupported
        report += 'wrong ext: %s\n' % self.wrong
        report += 'ignored(old): %s\n' % self.ignored
        report += 'elapsed time: (%s)\n' % (time() - self.time)

        print '='*80 + report + '='*80
        
                    
    def show_process_report(self):
        """
        Show process report
        """
        report = 'Processed: (%s), ' % self.processed
        report += 'ingested: (%s), ' % self.ingested
        report += 'unsupported: (%s), ' % self.unsupported
        report += 'wrong: (%s), ' % self.wrong
        report += 'ignored: (%s)' % self.ignored

        print report

class Ingester(threading.Thread):
    
    def __init__(self, queue, log, counter):
        self.log = log        
        self.queue = queue
        #--
        self.counter = counter
        #--
        self.db = OpenSyllabusDb(log)        
        self.extractor = TextExtractor(log)
        #--
        threading.Thread.__init__(self)


    def run(self):
        while True:
            data_file = self.queue.get()
            ext = get_file_ext(data_file)
            #--
            if ext and (ext in self.extractor.__class__.__dict__) and self.db.is_new(data_file):
                self.counter.inc_ing()
                file_type = get_file_type(data_file)
                data = getattr(self.extractor, file_type or ext)(data_file)
                self.db.insert_data(data_file, os.path.split(data_file)[1], data)
            else:
                if not ext:
                    self.counter.inc_wrong()
                elif ext not in self.extractor.__class__.__dict__:
                    self.counter.inc_unsupp()
                else:
                    self.counter.inc_ignore()
            #--
            self.counter.inc_proc()
            self.queue.task_done()

