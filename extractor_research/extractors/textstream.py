#!/usr/bin/python
import os

class TextStream:
    def __init__(self, pdf_file, txt_file):
        self.pdf_file = pdf_file
        self.txt_file = txt_file

    def extract(self):
        command = 'java -cp ./textstream:./textstream/lib/PDFTextStream.jar TextStream ' + self.pdf_file + ' ' + self.txt_file
        os.system(command)

if __name__ == '__main__': 
    pdf = TextStream('../input/pride_and_prej/1.pdf', '../output/pride_and_prej/textstream/1.txt')
    pdf.extract()