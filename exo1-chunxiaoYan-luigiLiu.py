#coding:utf-8

import codecs

def split(file) :

	"""
	split('sequoia-corpus.np_conll')
	trainc = read_corpus('sequoia-corpus.np_conll.train')
	devc = read_corpus('sequoia-corpus.np_conll.dev')
	testc = read_corpus('sequoia-corpus.np_conll.test')
	"""

	with codecs.open(file, encoding = 'utf-8') as f :
		sents = f.read().split(u'\n\n')
		n_sents = len(sents)

	subcorpus = u''
	for i,sent in enumerate(sents) :
		if subcorpus : subcorpus += u'\n\n'
		subcorpus += sent
		if i == n_sents * .8 :
			with codecs.open(file + u'.train', 'w', encoding = 'utf-8') as f :
				f.write(subcorpus)
				subcorpus = u''
		elif i == n_sents * .9 :
			with codecs.open(file + u'.dev', 'w', encoding = 'utf-8') as f :
				f.write(subcorpus)
				subcorpus = u''
	with codecs.open(file + u'.test', 'w', encoding = 'utf-8') as f :
		f.write(subcorpus)
		subcorpus = u''

def read_corpus(file) :

	with codecs.open(file, encoding = 'utf-8') as f :
		sent = u''
		sents = []
		for line in f :
			line = line.replace(u'\n','')
			if not line and sent : sents.append(sent); sent = u''
			else :
				cols = line.split()
				if sent : sent += u' '
				sent += u'/'.join([cols[1], cols[3]])
	return sents

if __name__ == '__main__' :

	split('sequoia-corpus.np_conll')
	trainc = read_corpus('sequoia-corpus.np_conll.train')
	devc = read_corpus('sequoia-corpus.np_conll.dev')
	testc = read_corpus('sequoia-corpus.np_conll.test')
	for sent in devc : print (sent)
