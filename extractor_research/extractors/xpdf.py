#!/usr/bin/python
import os

class XPDF:
    def __init__(self, pdf_file, txt_file, layout=True):
        self.pdf_file = pdf_file
        self.txt_file = txt_file
        # -layout : maintain original physical layout
        self.layout = layout

    def extract(self):
        if self.layout:
            command = 'pdftotext -layout ' + self.pdf_file + ' ' + self.txt_file
        else:
            command = 'pdftotext ' + self.pdf_file + ' ' + self.txt_file
        os.system(command)

if __name__ == '__main__': 
    pdf = XPDF('../input/pride_and_prej/1.pdf', '../output/pride_and_prej/xpdf/1.txt')
    pdf.extract()