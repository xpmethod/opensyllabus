"""
Author: Maxim Kosinov
Specialization: Python, HighLoad Crawlers, Data Mining, Scraping
E-Mail: astrey.labs@gmail.com
Skype: geminiozz
O-Desk: Astrey
"""

import os
import subprocess

from lxml import html
from lxml.html.clean import Cleaner
from pyPdf import PdfFileReader
from docx import opendocx, getdocumenttext

from opensyllabus.config import DATA_DIR
from opensyllabus.core.utils import clean_list, get_data_files, get_file_ext


class DataExtractor(object):
    """
    Class for extracting text data from pdf, doc/docx, html and other
    """

    def pdf(self, path):
        """
        Method for extracting text data from pdf files
        """
        pdf = PdfFileReader(file(os.path.join(DATA_DIR, path), 'rb'))
        return '\n'.join([page.extractText() for page in pdf.pages])
    

    def doc(self, path):
        """
        Method for extracting text data from doc files
        """
        p = subprocess.Popen(['antiword', os.path.join(DATA_DIR, path)], stdout=subprocess.PIPE)
        return p.communicate()[0]
        

    def docx(self, path):
        """
        Method for extracting text data from docx files
        """
        docx = opendocx(os.path.join(DATA_DIR, path))
        return '\n'.join([page for page in getdocumenttext(docx)])


    def html(self, path):
        """
        Method for extracting text data from html files
        """
        with open(os.path.join(DATA_DIR, path), 'r') as fh:
            cleaned = Cleaner(style=True).clean_html(fh.read())
            etree = html.fromstring(cleaned)
            return ' '.join(clean_list(etree.xpath('//text()')))
    
