#!/usr/bin/python
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, HTMLConverter, XMLConverter
from pdfminer.pdfpage import PDFPage

class Miner:
    def __init__(self, pdf_file, txt_file, file_format='txt', layout_analysis=True):
        self.pdf_file = file(pdf_file, 'rb')
        self.outfp = file(txt_file, 'w')

        if layout_analysis:
            laparams = LAParams()
        else:
            laparams = None

        self.rsrcmgr = PDFResourceManager(caching=True)
        
        if file_format == 'txt':
            self.device = TextConverter(self.rsrcmgr, self.outfp, codec='utf-8', 
                laparams=laparams, imagewriter=None)
        elif file_format == 'html':
            self.device = HTMLConverter(self.rsrcmgr, self.outfp, codec='utf-8', 
                laparams=laparams, imagewriter=None)
        elif file_format == 'xml':
            self.device = XMLConverter(self.rsrcmgr, self.outfp, codec='utf-8', 
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
    import os
    import re
    
    #converts pdfs in the input directory into html format
    pdfList = [('../input/%s' % f) for f in os.listdir('../input/') if '.pdf' in f]
    htmlList = [re.sub(r'.pdf', r'.xml', f) for f in pdfList]
    htmlList = [re.sub(r'input', r'output', f) for f in htmlList]
    
    for i in range(len(pdfList)):
        print 'converting: %s to %s' % (pdfList[i], htmlList[i])
        miner = Miner(pdfList[i], htmlList[i], file_format='xml')
        miner.extract()