import PyPDF2
import csv
import pdfminer
import os


def extract_text_using_pypdf(fileName):
	pdf = PyPDF2.PdfFileReader(open(fileName, "rb"))
	allText = []
	for page in pdf.pages:
		allText.append(page.extractText())
	return allText

def extract_text_using_pdf_miner(inputFile, outputFile):
	""" This method calls a command line argument from the pdfminer library
		Indicate txt or html by the file name output.txt or output.html
		For more commands, see http://www.unixuser.org/~euske/python/pdfminer/
	"""
	commandString = "pdf2txt.py -o " + outputFile + " " + inputFile
	os.system(commandString)

def export_to_csv(inputFileName, csvFileName):
	f = open(inputFileName, 'r')
	with open(csvFileName, 'wb') as csvfile:
		myWriter = csv.writer(csvfile, delimiter='\t')
		myWriter.writerow(f.readlines())

def test():
	#textVector = extract_text_using_pypdf("Lunch-Money.pdf")
	#export_to_csv(textVector[2:], "Lunch-Money.csv")
	extract_text_using_pdf_miner("E3562014236085.pdf", "E3562014236085.html")
	export_to_csv("E3562014236085.html", "E3562014236085.csv")


if __name__ == '__main__':
	test()
