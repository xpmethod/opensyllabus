#!/usr/bin/python

'''
https://stackoverflow.com/questions/582336/how-can-you-profile-a-python-script
(use with a second file option)
'''

from extractors import miner, pdf2, pdfbox, textstream, xpdf
import cProfile

def miner_with_layout(pdf_file, txt_file):
    pdf = miner.Miner(pdf_file, txt_file)
    pdf.extract()

def miner_without_layout(pdf_file, txt_file):
    pdf = miner.Miner(pdf_file, txt_file, layout_analysis=False)
    pdf.extract()

def xpdf_with_layout(pdf_file, txt_file):
    pdf = xpdf.XPDF(pdf_file, txt_file)
    pdf.extract()

def xpdf_without_layout(pdf_file, txt_file):
    pdf = xpdf.XPDF(pdf_file, txt_file, layout=False)
    pdf.extract()

def textstream_default(pdf_file, txt_file):
    pdf = textstream.TextStream(pdf_file, txt_file)
    pdf.extract()

def pdf2_default(pdf_file, txt_file):
    pdf = pdf2.PDF2(pdf_file, txt_file)
    pdf.extract()

def pdfbox_default(pdf_file, txt_file):
    pdf = pdfbox.PDFBox(pdf_file, txt_file)
    pdf.extract()

def run_all(pdf_file, txt_file):
    miner_with_layout(pdf_file, txt_file)
    miner_without_layout(pdf_file, txt_file)
    xpdf_with_layout(pdf_file, txt_file)
    xpdf_without_layout(pdf_file, txt_file)
    textstream_default(pdf_file, txt_file)
    pdf2_default(pdf_file, txt_file)
    pdfbox_default(pdf_file, txt_file)

def time_all(pdf_file, txt_file):
    cProfile.run('miner_with_layout(pdf_file, txt_file)')
    cProfile.run('miner_without_layout(pdf_file, txt_file)')
    cProfile.run('xpdf_with_layout(pdf_file, txt_file)')
    cProfile.run('xpdf_without_layout(pdf_file, txt_file)')
    cProfile.run('textstream_default(pdf_file, txt_file)')
    cProfile.run('pdf2_default(pdf_file, txt_file)')
    cProfile.run('pdfbox_default(pdf_file, txt_file)')

if __name__ == '__main__': 
    pdf_file = './input/pride_and_prej/1.pdf'
    txt_file = 'tester.txt'
    time_all(pdf_file, txt_file)