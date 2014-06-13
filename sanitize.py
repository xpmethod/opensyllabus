import re

class Sanitize(object):

	"""
		Methods for removing personal information from a syllabus.
	"""

	@classmethod
	def get_professor_names(cls, text):
		''' Find phrases that begin with Dr., Prof., Professor, or Instructor 
			and then 1-3 words in title case '''
		matches = re.findall(r"(.)*((Prof\.)|(Dr\.)|(Professor)|(Instructor(:)*))(((\ ){0,2}([A-Z][a-z]{2,})*){1,3})", text)
		#print matches
		fullPhrases = []
		for m in matches:
			full = m[7].strip()
			if full and ( full not in fullPhrases ) :
				fullPhrases.append(full)
		return fullPhrases

	@classmethod
	def get_email_addresses(cls, text):
		''' Find phrases that contain @ symbol '''
		matches = re.findall(r"(.)*(\b(\w|\.)+@(\w|\.)+\b)(.)*", text)
		fullPhrases = []
		for m in matches:
			full = m[1]
			if full and ( full not in fullPhrases ) :
				fullPhrases.append(full)
		return fullPhrases

	@classmethod
	def get_phone_numbers(cls, text):
		''' Find phrases in the form 555-555-5555 or (555)555-5555 '''
		matches = re.findall(r"(.)*(([0-9]{3}[\-]|\([0-9]{3}\))[0-9]{3}[\-][0-9]{4})(.)*", text)
		fullPhrases = []
		for m in matches:
			full = m[1]
			if full and ( full not in fullPhrases ) :
				fullPhrases.append(full)
		#print fullPhrases
		return fullPhrases

	@classmethod
	def remove_names_and_emails_and_phone(cls, text):
		""" Deletes instances of professor names, emails, and phone numbers from the text """
		## Our approach is to make a regular expression that will replace any
		## character name that is in either 'FULL CAPS' or in 'Title Case'
		## "(JOHN)|(John)|(ALICE)|(Alice)", etc.
		emails = Sanitize.get_email_addresses(text)
		names = Sanitize.get_professor_names(text)
		phone = Sanitize.get_phone_numbers(text)
		allToRemove = emails + names + phone
		withParens = map(lambda x: "(" + x + ")", allToRemove)
		for regex in withParens:
			text = re.sub(regex, "", text)
		return text
		#print text

def sanitize_test():
	PRACTICE_TEXT = " HIST101 \n Dr. Eddard Stark \n Winterfell College \n Phone: 212-555-5555 \n Email: ned@kingslanding.edu \n Hand of the King.\n\n\n"
	print PRACTICE_TEXT
	print Sanitize.remove_names_and_emails_and_phone(PRACTICE_TEXT)

if __name__ == '__main__':
	sanitize_test()
	
	
	
######################################################################################################
##
##    This code was written by:
##
##              Graham Sack
##          Columbia University
##    http://www.columbia.edu/~gas2117/grahamsack.html
##
#####################################################################################################

