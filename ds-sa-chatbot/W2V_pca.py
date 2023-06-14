#model = gensim.models.Word2Vec.load('ko/ko.bin')
#model = gensim.models.KeyedVectors.load_word2vec_format('ko/ko.bin', encoding='utf8')
#Pretrained W2V: https://github.com/Kyubyong/wordvectors

#https://drive.google.com/file/d/1ZiDi_xvqzUvmf7MqLn4AgB9VRQ5rPKRd/view?usp=drive_link


import gensim
import numpy as np
import csv
import re
from sklearn import manifold

EMB_SIZE = 128

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

## pca to reduce dimensionality from 200 to ??
vectors = np.array(vectors)
pca = manifold.TSNE(perplexity=40, n_components=EMB_SIZE, method='exact', init='pca')
vectors = pca.fit_transform(vectors)

model = gensim.models.keyedvectors.KeyedVectors(EMB_SIZE, dtype=float)
model.add_vectors(keys, vectors)
model.save('ko_pca.kv')
print(model.vectors.shape)