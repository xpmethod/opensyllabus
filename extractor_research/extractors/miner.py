#!/usr/bin/python
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage

class Miner:
    def __init__(self, pdf_file, txt_file, layout_analysis=True):
        self.pdf_file = file(pdf_file, 'rb')
        self.outfp = file(txt_file, 'w')

        if layout_analysis:
            laparams = LAParams()
        else:
            laparams = None

        self.rsrcmgr = PDFResourceManager(caching=True)
        self.device = TextConverter(self.rsrcmgr, self.outfp, codec='utf-8', 
            laparams=laparams, imagewriter=None)

    def extract(self):
        interpreter = PDFPageInterpreter(self.rsrcmgr, self.device)
        pagenos = set()
        for page in PDFPage.get_pages(self.pdf_file, pagenos, maxpages=0, 
            password=None, caching=True, check_extractable=True):
            interpreter.process_page(page)
        self.pdf_file.close()
        self.device.close()
        self.outfp.close()

if __name__ == '__main__': 
    miner = Miner('../input/pride_and_prej/1.pdf', '../output/pride_and_prej/miner/1.txt')
    miner.extract()