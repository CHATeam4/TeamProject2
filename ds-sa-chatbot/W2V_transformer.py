#model = gensim.models.Word2Vec.load('ko/ko.bin')
#model = gensim.models.KeyedVectors.load_word2vec_format('ko/ko.bin', encoding='utf8')
#Pretrained W2V: https://github.com/Kyubyong/wordvectors

import gensim
import numpy as np
import csv
import re

keys=[]
vectors=[]
with open('ko/ko.tsv') as f:
	tr = csv.reader(f, delimiter='\t')
	i=0
	for row in tr:
		if i==0:
			keys.append(row[1])
			rr = re.sub('\[', '', row[2])
			rows=list(rr.split())
		else:
			rr = re.sub('\]', '', row[0])
			rows+=list(rr.split())
		i=len(rows)
		if i>=200:
			i=0
			arr=np.array(rows).astype(np.float64)
			vectors.append(arr)

model = gensim.models.keyedvectors.KeyedVectors(200, dtype=float)
model.add_vectors(keys, vectors)
model.save('ko.kv')