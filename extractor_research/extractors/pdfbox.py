#!/usr/bin/python
import os

class PDFBox:
    def __init__(self, pdf_file, txt_file):
        self.pdf_file = pdf_file
        self.txt_file = txt_file

    def extract(self):
        # need to hardcode path because of imports
        command = 'java -jar ~/workspace/OSP/opensyllabus/extractor_research/extractors/pdfbox-app-1.8.5.jar ExtractText ' + self.pdf_file + ' ' + self.txt_file
        os.system(command)

if __name__ == '__main__': 
    pdf = PDFBox('../input/pride_and_prej/1.pdf', '../output/pride_and_prej/pdfbox/1.txt')
    pdf.extract()