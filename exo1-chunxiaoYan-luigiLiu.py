#coding:utf-8

import codecs

def split(file, ratio = [80, 10, 10]) :

	files_out = [file + u'.train',\
                     file + u'.dev'  ,\
	             file + u'.test']

	with codecs.open(file, encoding = 'utf-8') as f :
		sents = f.read().split(u'\n\n')

	subcorpus = []
	cursor = 0
	for sent in sents :
		subcorpus.append(sent)
		if len(subcorpus) * sum(ratio) >= len(sents) * ratio[cursor] :
			with codecs.open(files_out[cursor], 'w', 'utf-8') as f :
				f.write(u'\n\n'.join(subcorpus))
				subcorpus = []
			cursor += 1

	if subcorpus :
		with codecs.open(files_out[cursor], 'w', encoding = 'utf-8') as f :
			f.write(subcorpus)


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
