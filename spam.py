import sys
import collections
import re
import glob
import errno
from math import exp, log

class SpamFilter(object):
	def __init__(self, pSpam):
		self.pSpam = pSpam
		self.pHam = 1 - pSpam
		self.spam = collections.Counter()
		self.totalSpam = 0
		self.ham = collections.Counter()
		self.totalHam = 0
		self.minValue = 1e-12
		self.maxValue = 1 - (1e-12)

	def train_spam(self, fileSpam):
		"""Creates the Dictionary for Spam Words"""
		for name in fileSpam:
			with open(name) as f:
				s = collections.Counter(
					word.lower()
					for line in f
					for word in re.findall(r'\b[^\W_]+\b', line))
				self.spam.update(s)
		self.totalSpam = sum(self.spam.values())

	def train_ham(self, fileHam):
		"""Creates the Dictionary for Ham Words"""
		for name in fileHam:
			with open(name) as f:
				h = collections.Counter(
					word.lower()
					for line in f
					for word in re.findall(r'\b[^\W_]+\b', line))
				self.ham.update(h)
		self.totalHam = sum(self.ham.values())

	def spam_to_file(self):
		outSpam = open('outputSpam.txt', 'w')
		outSpam.write('%d\n' % self.totalSpam)
		for word, count in self.spam.most_common():
			pBA = float(count)/self.totalSpam		#P(word|spam)
			pAB = self.p_spam_given_word(word)
			outSpam.write('%s: %d \tP(word|spam): %f \tP(spam|word): %f\n' % (word, count, pBA, pAB))

	def ham_to_file(self):
		outHam = open('outputHam.txt', 'w')
		outHam.write('%d\n' % self.totalHam)
		for word, count in self.ham.most_common():
			pBA = float(count)/self.totalHam		#P(word|ham)
			pAB = self.p_spam_given_word(word)
			outHam.write('%s: %d \tP(word|ham): %f \tP(ham|word): %f\n' % (word, count, pBA, pAB))

	def p_spam_given_word(self, word):
		#Baye's Theorem Calculation

		if self.spam[word] == 0:
			return 0.1
		elif self.ham[word] == 0:
			return 0.9

		if self.spam[word] + self.ham[word] < 10:
			return 0.5

		pWordSpam = float(self.spam[word])/self.totalSpam		#P(word|spam)
		pWordHam = float(self.ham[word])/self.totalHam
		pSpamWord = (pWordSpam * self.pSpam)/((pWordSpam*self.pSpam)+(pWordHam*self.pHam))	#P(spam|word)

		return pSpamWord

	def p_spam(self, file):
		n = 0
		with open(file) as f:
			for line in f:
				for word in re.findall(r'\b[^\W_]+\b', line):
					word.lower()
					pAB = self.p_spam_given_word(word)
					n += (log(1-pAB)-log(pAB))
		
		if n > 200:
			probability = 1/(1+exp(200))
		else:
			probability = 1/(1+exp(n))
		
		return probability


if __name__ == '__main__':
	fileSpam = glob.glob('./learning_spam/*')
	fileHam = glob.glob('./learning_ham/*')
	fileTestSpam = glob.glob('./test_spam/*')
	fileTestHam = glob.glob('./test_ham/*')
	fileTest = glob.glob('./test/*')
	
	spamFilter = SpamFilter(0.75)
	spamFilter.train_spam(fileSpam)
	spamFilter.train_ham(fileHam)
	spamFilter.spam_to_file()
	spamFilter.ham_to_file()

	spamCount = 0
	hamCount = 0

	for name in fileTest:
		if spamFilter.p_spam(name) > 0.90:
			spamCount += 1
			print "%s is SPAM" % name
		else:
			hamCount += 1
			print "%s is HAM" % name