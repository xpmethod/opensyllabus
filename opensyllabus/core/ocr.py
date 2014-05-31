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
import glob
import logging
import subprocess

# add project dir to PYTHONPATH
sys.path.insert(0, os.path.split(os.path.split(sys.path[0])[0])[0])

from opensyllabus.config import TMP_DIR


class OpenSyllabusOCR(object):
    
    def __init__(self):
        self.ex_txt = ''

        
    def extract(self, input_pdf):
        """
        Extract images from pdf file and then extract text from them
        Input: full path to pdf file
        Output: return extracted text, otherwise return False
        """
        glob_img_filename = self._extract_images(input_pdf)
        if glob_img_filename:
            return self._extract_text(glob_img_filename)
        return False
    
    
    def _delete_tmp_files(self, img_file, txt_file):
        """
        Delete temporary files
        Input: path to image file and path to txt file
        Output: None
        """
        for tmp_file in (img_file, txt_file):
            try:
                os.remove(tmp_file)
            except IOError as e:
                logging.exception(e)        
    
        
    def _extract_images(self, input_pdf):
        """
        Extract images from pdf file and save them to hdd
        Input: full path to pdf file
        Output: pathname pattern for extracted images
        """
        pdf_dir, pdf_filename = os.path.split(input_pdf)
        pdf_name, pdf_ext = os.path.splitext(pdf_filename)
        output_filename = os.path.join(TMP_DIR, pdf_name) 
        # compose cmd string
        cmd = 'gs -q -dNOPAUSE -sDEVICE=pngmono -r300 -sOutputFile="%s_%%d.png" "%s" -c quit' % (output_filename, input_pdf)

        try:
            subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            logging.exception(e)
        else:        
            return '%s_*.png' % output_filename


    def _extract_text(self, glob_img_filename):
        """
        Extract text from images and save it to files
        Input: pathname pattern for extracted images
        Output: return extracted text
        """
        for i, img_file in enumerate(glob.glob(glob_img_filename)[::-1], 1):
            img_dir, img_filename = os.path.split(img_file)
            img_name, img_ext = os.path.splitext(img_filename)
            output_filename = os.path.join(TMP_DIR, img_name)
            # compose cmd string
            cmd = 'tesseract "%s" "%s"' % (img_file, output_filename)
            
            try:
                subprocess.check_output(cmd, shell=True)
            except subprocess.CalledProcessError as e:
                logging.exception(e)
            else:
                # add extension to output filename
                txt_file = '%s.txt' % output_filename
                
                # read text from file to buffer
                with open(txt_file, 'r') as fh:
                    self.ex_txt += ' %s' % fh.read()
                    
                # delete tmp files
                self._delete_tmp_files(img_file, txt_file)
                        
        return self.ex_txt

        
if __name__ == '__main__':
    ocr = OpenSyllabusOCR()
    print ocr.extract('/home/qnx/My Work/projects/opensyllabus/_data/mikes-collection/emory_050000003538.pdf')
    
    