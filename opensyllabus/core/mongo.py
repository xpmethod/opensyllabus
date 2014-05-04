# -*- coding:utf8 -*-
"""
Author: Maxim Kosinov
Specialization: Python, HighLoad Crawlers, Data Mining, Scraping
E-Mail: astrey.labs@gmail.com
Skype: geminiozz
O-Desk: Astrey
"""

import os
import bson 
from pymongo import MongoClient, ASCENDING, DESCENDING

from opensyllabus.config import MONGODB_HOST, MONGODB_PORT


class OpenSyllabusDb(object):
    
    def __init__(self):
        self._init_connection()
    
    def _init_connection(self):
        # connect to mongodb server
        self.client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        # select mongodb database with name denten_crawler
        self.db = self.client['opensyllabus']
        # set collection name
        self.collection = self.db['opensyllabus']
        
    def insert_data(self, path, filename, data):
        mongo_item = {
            'path': path,
            'filename': filename,
            'data': data,
        }
        # insert data to collection
        self.collection.insert(mongo_item)
              
        
    def is_new(self, filepath):
        """
        Return True if data file is new, otherwise return False
        """
        if not self.collection.find({'path': filepath}).count():
            return True
        return False
        
