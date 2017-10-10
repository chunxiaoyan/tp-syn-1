#! /usr/bin/env python3
#coding:utf-8


from SparseWeightVector import SparseWeightVector
from math import exp,log
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
	
class AvgPerceptron:

    def __init__(self):
        
        self.model   = SparseWeightVector()
        self.Y       = [] #classes

    def train(self,dataset,step_size=0.1,max_epochs=50):

        model_acc = None
        self.Y = list(set([y for (y,x) in dataset]))

        for e in range(max_epochs):
            
            loss = 0.0            
            e = 0
            for y,x in dataset:
                ypred = self.tag(x)
                if y != ypred:
                    loss += 1.0
                    delta_ref  = SparseWeightVector.code_phi(x,y)
                    delta_pred = SparseWeightVector.code_phi(x,ypred)
                    self.model += step_size*(delta_ref-delta_pred)
		    # la moyenne du passé accumulé des poids
                    if not model_acc : self.model_acc = self.model; e+=1
                    else : model_acc += self.model; e+=1 ; self.model = model_acc * (1 / float(e))
            print ("Loss (#errors) = ",loss)
            if loss == 0.0:
                return
                     
    def predict(self,dataline):
        return list([self.model.dot(dataline,c) for c in self.Y])
    
    def tag(self,dataline):

        scores = self.predict(dataline)
        imax   = scores.index(max(scores)) 
        return self.Y[ imax ]

    def test(self,dataset):

        result = list([ (y == self.tag(x)) for y,x in dataset ])
        return sum(result) / len(result)

if __name__ == '__main__' :

	split('sequoia-corpus.np_conll')
	trainc = read_corpus('sequoia-corpus.np_conll.train')
	devc = read_corpus('sequoia-corpus.np_conll.dev')
	testc = read_corpus('sequoia-corpus.np_conll.test')

	p = AvgPerceptron()
	p.train(trainc)
	print(p.test(testc))
	
