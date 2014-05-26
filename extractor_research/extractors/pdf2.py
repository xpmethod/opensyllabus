#!/usr/bin/python
from PyPDF2 import PdfFileReader

class PDF2:
    def __init__(self, pdf_file, txt_file):
        self.doc = PdfFileReader(open(pdf_file, 'rb'))
        self.output = open(txt_file, 'w')

    def extract(self):
        for page in self.doc.pages:
            self.output.write(page.extractText())
        self.output.close()

if __name__ == '__main__': 
    pdf = PDF2('../input/pride_and_prej/1.pdf', '../output/pride_and_prej/pdf2/1.txt')
    pdf.extract()