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

from lxml import html
from lxml.html.clean import Cleaner
from pyPdf import PdfFileReader
from docx import opendocx, getdocumenttext

from opensyllabus.config import DATA_DIR
from opensyllabus.core.utils import clean_list, get_data_files, get_file_ext
from opensyllabus.core.ocr import OpenSyllabusOCR


class TextExtractor(object):
    """
    Class for extracting text data from pdf, doc/docx, html and other
    """
    
    def __init__(self, log):
        self.log = log
        self.ocr = OpenSyllabusOCR(log)


    def pdf(self, path):
        """
        Method for extracting text data from pdf files
        Input: full path to pdf file
        Output: extracted text        
        """
        try:
            pdf = PdfFileReader(file(os.path.join(DATA_DIR, path), 'rb'))
            text = '\n'.join([page.extractText() for page in pdf.pages])
        except Exception as e:
            self.log.exception(e)
        else:
            if not re.sub('[\n]+', '', text):
                return self.ocr.extract(os.path.join(DATA_DIR, path))
            return text 
    

    def doc(self, path):
        """
        Method for extracting text data from doc files
        Input: full path to doc file
        Output: extracted text        
        """
        try:
            p = subprocess.Popen(['antiword', os.path.join(DATA_DIR, path)], stdout=subprocess.PIPE)
            text = p.communicate()[0]
        except Exception as e:
            self.log.exception(e)
        else:
            return text
        

    def docx(self, path):
        """
        Method for extracting text data from docx files
        Input: full path to docx file
        Output: extracted text
        """
        try:
            docx = opendocx(os.path.join(DATA_DIR, path))
            text = '\n'.join([page for page in getdocumenttext(docx)])
        except Exception as e:
            self.log.exception(e)
        else:
            return text

    
    def htm(self, path):
        """
        Method for extracting text data from htm files
        Input: full path to htm file
        Output: extracted text
        """
        return self.html(path)


    def html(self, path):
        """
        Method for extracting text data from html files
        Input: full path to html file
        Output: extracted text
        """
        try:
            fh = open(os.path.join(DATA_DIR, path), 'r')
            etree = html.fromstring(Cleaner(style=True).clean_html(fh.read()))
            text = ' '.join(clean_list(etree.xpath('//text()')))
        except Exception as e:
            self.log.exception(e)
        else:
            return text

