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
from opensyllabus.core.exceptions import WrongFileExtension

def clean_list(in_list):
    return [re.sub('[\r\n\t ]+', ' ', el.strip()) for el in in_list if re.sub('[\r\n\t ]+', '', el)]

def get_data_files():
    for top_dir in os.listdir(DATA_DIR):
        if not ('cohen-archive' in top_dir):
            for r, dirs, files in os.walk(os.path.join(DATA_DIR, top_dir)):
                for data_file in files:
                    yield os.path.join(r, data_file)
        else:
            archive_path = os.path.join(DATA_DIR, top_dir, 'web.archive.org', 'web')
            p = subprocess.Popen(['ls', '-f', archive_path], stdout=subprocess.PIPE)
            for dir in p.communicate()[0].split('\n'):
                if dir not in ['.', '..']:
                    for r, dirs, files in os.walk(os.path.join(archive_path, dir)):
                        for data_file in files:
                            yield os.path.join(r, data_file)                
                

def get_file_dir(filepath):
    data_dir = os.path.split(DATA_DIR)[1]
    dirs = filepath.split('/')
    return dirs[dirs.index(data_dir) + 1] 
    
            
def get_file_ext(filename):
    ext = os.path.splitext(filename)[1].lower()
    if 7 > len(ext) > 1:
        return ext[1:]

    raise WrongFileExtension
            