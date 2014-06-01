#!/usr/bin/python

'''
https://stackoverflow.com/questions/582336/how-can-you-profile-a-python-script
(use with a second file option)
'''

from extractors import miner, pdf2, pdfbox, textstream, xpdf
import cProfile

def miner_with_layout(pdf_file, txt_file):
    miner = miner.Miner(pdf_file, txt_file)
    miner.extract()

def miner_without_layout(pdf_file, txt_file):
    miner = miner.Miner(pdf_file, txt_file, layout_analysis=False)
    miner.extract()

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