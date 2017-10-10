#coding:utf-8

import codecs

# function repise et légèrement modifiée de celle intitulée make_dataset dans Multiclass.py
# modification portant un problème posé quand '/' figure aussi dans le token 
def make_dataset_customed(text):
    """
    @param text: a list of strings of the form : Le/D chat/N mange/V la/D souris/N ./PONCT
    @return    : an n-gram style dataset
    """
    BOL = '@@@'
    EOL = '$$$'

    def sep_token_pos(token_pos) :
        tmp = token_pos.split(u'/')
        return tuple([u'/'.join(tmp[:-1]),tmp[-1]])

    dataset = []
    for line in text:
        line         = list([sep_token_pos(w) for w in line.split()])
        tokens       = [BOL] + list([tok for(tok,pos) in line]) + [EOL]
        pos          = list([pos for(tok,pos) in line]) 
        tok_trigrams = list(zip(tokens,tokens[1:],tokens[2:]))
        tok_bigramsL = list(zip(tokens,tokens[1:]))
        tok_bigramsR = list(zip(tokens[1:],tokens))
        
        dataset.extend(zip(pos,zip(tok_trigrams,tok_bigramsL,tok_bigramsR)))
                
    return dataset

def split(file, ratio = [80, 10, 10], limit = -1) :

	fout   = [file + u'.train', file + u'.dev', file + u'.test']
	corpus = [              [],             [],              []]

	with codecs.open(file, encoding = 'utf-8') as f :
		allsents = f.read().split(u'\n\n')

	# échantillonnage dynamique or waterfill method
	for sent in allsents :
		if   not corpus[0] : corpus[0].append(sent)
		elif not corpus[1] : corpus[1].append(sent)
		elif not corpus[2] : corpus[2].append(sent)
		else :
			want = [ratio[0] * len(corpus[1]) * len(corpus[2]),\
			 	ratio[1] * len(corpus[0]) * len(corpus[2]),\
				ratio[2] * len(corpus[0]) * len(corpus[1])]
			want_id = sorted(zip(range(3), want), key = lambda x : x[1], reverse = True)[0][0]
			corpus[want_id].append(sent)

		lenc = sum([len(corpora) for corpora in corpus])
		if lenc >= limit and limit > 0 : break

	for file, corpora in zip(fout, corpus) :
		with codecs.open(file, 'w', 'utf-8') as f :
			f.write(u'\n\n'.join(corpora))


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
	return make_dataset_customed(sents)

if __name__ == '__main__' :

	split('sequoia-corpus.np_conll')
	trainc = read_corpus('sequoia-corpus.np_conll.train')
	devc = read_corpus('sequoia-corpus.np_conll.dev')
	testc = read_corpus('sequoia-corpus.np_conll.test')
	
