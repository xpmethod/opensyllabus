import textblob
import numpy

class Document(object):

	STOPWORDS = "are you my I a and these to it with me your not but him do so"

	@classmethod
	def make_stop_words(cls, stopwords):
		return stopwords.lower().split()

	def __init__(self, text, label=None):
		self.text = text
		self.label = label
		self.stopwords = Document.make_stop_words(Document.STOPWORDS)
		self.wordVector = None

	def get_label(self):
		return self.label

	def split_and_remove_stop_words(self):
		## split and make all the words lower case
		splitText = self.text.lower().split()
		scrubbedText = []
		for word in splitText:
			if word not in self.stopwords:
				scrubbedText.append(word)
		self.wordVector = scrubbedText

	def count_tokens(self):
		return len(self.wordVector)

	def get_word_frequencies(self):
		wordFreq = {}
		for word in self.wordVector:
			if word not in wordFreq:
				wordFreq[word] = 1
			else:
				wordFreq[word] += 1
		return wordFreq

	def get_vocabulary(self):
		wordFreq = self.get_word_frequencies()
		return wordFreq.keys()

class DocDatabase(object):

	def __init__(self, documents):
		self.documents = documents
		self.classes = self.get_classes()
		self.vocabulary = self.construct_complete_vocabulary()
		self.priorProbs = self.calc_prior_probs()
		self.conditionalProbs = self.calc_conditional_prob_per_word()

	def get_classes(self):
		classes = []
		for d in self.documents:
			label = d.get_label()
			if label not in classes:
				classes.append(label)
		return classes

	def count_docs_per_class(self):
		""" Determine the number of documents per class """
		classCounts = { c:0 for c in self.classes }
		for d in self.documents:
			label = d.get_label()
			classCounts[label] += 1
		return classCounts

	def calc_prior_probs(self):
		""" Determine the probabilty of each class. This is also known as the
			prior probability. """
		classCounts = self.count_docs_per_class()
		totalNumTexts = sum(classCounts.values())
		classProbs = { c:( classCounts[c] / float(totalNumTexts) ) for c in classCounts.keys() }
		return classProbs

	def construct_complete_vocabulary(self):
		""" Generate a complete list of vocabulary words across all documents """
		vocab = set([])
		for d in self.documents:
			vocab = vocab.union(set(d.get_vocabulary()))
		return vocab

	def calc_word_freq_per_class(self):
		""" Determine the word frequencies for each class  """
		classVocab = {}
		for c in self.classes:
			## initialize the word frequencies to 0
			classVocab[c] = { word:0 for word in self.vocabulary }
		for d in self.documents:
			myClass = classVocab[d.get_label()]
			myFrequencies = d.get_word_frequencies()
			for word in myFrequencies.keys():
				myClass[word] += myFrequencies[word]
		return classVocab

	def count_tokens_per_class(self):
		countTokens = { c:0 for c in self.classes }
		for d in self.documents:
			countTokens[d.get_label()] += d.count_tokens()
		return countTokens

	def calc_conditional_prob_per_word(self):
		""" We will use LAPLACE ADD-1 SMOOTHING:
		p(word | class ) =  [ # of tokens of word in class ) + 1 ] / [ ( total number of tokens in class ) + VOCAB_SIZE] """
		conditionalProbs = self.calc_word_freq_per_class()
		countTokens = self.count_tokens_per_class()
		for c in conditionalProbs.keys():
			for w in conditionalProbs[c].keys():
				conditionalProbs[c][w] = float( conditionalProbs[c][w] + 1) / float( countTokens[c] + len(self.vocabulary))
		return conditionalProbs

	def prior_prob(self, givenClass):
		return self.priorProbs[givenClass]

	def conditional_prob(self, givenClass, word):
		## if the word is actually contained in the known vocabulary for the class, 
		## return the conditional probability
		if word in self.conditionalProbs[givenClass].keys():
			return self.conditionalProbs[givenClass][word]
		## if the word is unknown, then use the following smoothing approximation
		## Pr(word) = 1 / ( VOCAB-SIZE + 1 )
		else:
			return 1 / float(len(self.vocabulary) + 1)


	def classify(self, testDoc):
		""" Given a test document, determine the most probable classification """
		## Get the word frequencies for the document
		doc = Document(testDoc)
		doc.split_and_remove_stop_words()
		docWordFreqs = doc.get_word_frequencies()
		docWords = docWordFreqs.keys()
		## P(c|w) = [ P(w|c) ^ (count_w) ] * P(c)
		results = {}
		for c in self.classes:
			productOfConditionals = numpy.prod(map(lambda x: self.conditional_prob(c,x) ** docWordFreqs[x], docWords))
			probOfClass = productOfConditionals * self.prior_prob(c)
			results[c] = probOfClass
		bestLabel = max( results.items(), key=lambda x: x[1])
		return bestLabel[0]

	def classify_test_set(self, testSet):
		return map(lambda x: self.classify(x), testSet)


def test_doc():
	class1 = [ "How are you my friends I brought you a sandwich", 
		"I found a sandwich and these beers and I wanted to know you wanted to share it with me", 
		"Listen my friend I going to get a beer tonight you want to join me" ]
	class2 = [ "Friends Romans countryman lend me your ears", 
		"I come not to praise caesar but to bury him gentle romans", 
		"mighty caesar do you lie so low" ]
	testSet = [ "Beers sandwich tonight", "caesar romans beers", "bury bury friends sandwiches share" ]
	documents = []
	for doc in class1:
		docObject = Document(doc, 'class1')
		docObject.split_and_remove_stop_words()
		documents.append(docObject)
	for doc in class2:
		docObject = Document(doc, 'class2')
		docObject.split_and_remove_stop_words()
		documents.append(docObject)

	myDD = DocDatabase(documents)
	myDD.construct_complete_vocabulary()
	print myDD.classify_test_set(testSet)
	#print myDD.documents
	#print myDD.get_classes()
	#print myDD.vocabulary
	#print myDD.calc_word_freq_per_class()
	#print myDD.count_tokens_per_class()
	#print myDD.calc_conditional_prob_per_word()
	
	"""
	doc1 = Document(class1[0], 'class1')
	doc1.split_and_remove_stop_words()
	print doc1.wordVector
	print doc1.count_tokens()
	print doc1.get_word_frequencies()
	print doc1.get_vocabulary()
	"""

test_doc()
