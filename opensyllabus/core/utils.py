# -*- coding:utf8 -*-
"""
Author: Maxim Kosinov
Specialization: Python, HighLoad Crawlers, Data Mining, Scraping
E-Mail: astrey.labs@gmail.com
Skype: geminiozz
O-Desk: Astrey
"""

import os
import re
import subprocess

from opensyllabus.config import DATA_DIR


def clean_list(in_list):
    """
    Remove special symbols on each elemnt in the list
    Input: list
    Output: list with cleaned elements
    """
    return [re.sub('[\r\n\t ]+', ' ', el.strip()) for el in in_list if re.sub('[\r\n\t ]+', '', el)]


def get_data_files_2():
    """
    Walking over data directories and return data files
    Input: None
    Output: iterator with pathes to data files
    """
    for i in range(1):
        for top_dir in os.listdir(DATA_DIR):
            for r, dirs, files in os.walk(os.path.join(DATA_DIR, top_dir)):
                for data_file in files:
                    yield os.path.join(r, data_file)
                    
def get_data_files():
    """
    Walking over data directories and return data files
    Input: None
    Output: iterator with pathes to data files
    """
    for top_dir in os.listdir(DATA_DIR):
        if not ('cohen-archive' in top_dir):
            for r, dirs, files in os.walk(os.path.join(DATA_DIR, top_dir)):
                for data_file in files:
                    yield os.path.join(r, data_file)
        else:
            # trick for walk over big directories
            archive_path = os.path.join(DATA_DIR, top_dir, 'web.archive.org', 'web')
            p = subprocess.Popen(['ls', '-f', archive_path], stdout=subprocess.PIPE)
            for dir in p.communicate()[0].split('\n'):
                if dir not in ['.', '..']:
                    for r, dirs, files in os.walk(os.path.join(archive_path, dir)):
                        for data_file in files:
                            yield os.path.join(r, data_file)                
                

def get_file_dir(filepath):
    """
    Return root directory for the file
    Input: full path to file
    Output: root directory
    """
    data_dir = os.path.split(DATA_DIR)[1]
    dirs = filepath.split('/')
    return dirs[dirs.index(data_dir) + 1] 
    
            
def get_file_ext(filename):
    """
    Return file extension
    Input: filename
    Output: file extension
    """
    ext = os.path.splitext(filename)[1].lower()
    if 7 > len(ext) > 1:
        return ext[1:]
            