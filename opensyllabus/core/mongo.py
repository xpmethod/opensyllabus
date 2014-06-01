# -*- coding:utf8 -*-
"""
Author: Maxim Kosinov
Specialization: Python, HighLoad Crawlers, Data Mining, Scraping
E-Mail: astrey.labs@gmail.com
Skype: geminiozz
O-Desk: Astrey
"""

import os
from pymongo import MongoClient, ASCENDING, DESCENDING

from opensyllabus.config import MONGODB_HOST, MONGODB_PORT


class OpenSyllabusDb(object):
    
    def __init__(self, log):
        self.log = log
        self._init_connection()
    
    def _init_connection(self):
        """
        Initilize connection to MongoDB
        Input: None
        Output: None
        """
        try:
            # connect to mongodb server
            self.client = MongoClient(MONGODB_HOST, MONGODB_PORT)
            # select mongodb database with name denten_crawler
            self.db = self.client['opensyllabus']
            # set collection name
            self.collection = self.db['opensyllabus']
        except Exception as e:
            self.log.exception(e)
            
            
    def insert_data(self, path, filename, text):
        """
        Insert extracted text to db
        Input: path - full path to file
               filename - data file name
               text - extracted text
        Output: None
        """
        mongo_item = {
            'path': path,
            'filename': filename,
            'text': text,
        }
        try:
            # insert data to collection
            self.collection.insert(mongo_item)
        except Exception as e:
            self.log.exception(e)
              
        
    def is_new(self, filepath):
        """
        Check file for exists in db
        Input: full path to data file
        Output: return True if file doesn't exist in db, otherwise return False
        """
        if not self.collection.find({'path': filepath}).count():
            return True
        return False
        
