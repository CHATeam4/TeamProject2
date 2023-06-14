# 필요한 모듈 임포트
import pandas as pd
import tensorflow as tf
import numpy as np
import gensim
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate
import os

kv=gensim.models.keyedvectors.KeyedVectors.load('ko.kv')


# 말뭉치 데이터 읽어오기
def read_corpus_data(filename):
    with open(filename, 'r') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
    return data


# 말뭉치 데이터 가져오기
corpus_data = read_corpus_data('./train_tools/dict/corpus.txt')


from utils.Preprocess import Preprocess
p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
               userdic='utils/user_dic.tsv')

keywords=[]
for sentence in corpus_data:
    pos = p.pos(sentence[1])
    keywords.append(p.get_keywords(pos, without_tag=True))

#W2V모델 생성 후 기존 데이터 탑재
model = gensim.models.Word2Vec(['OOV'], vector_size=200, min_count=1, negative=5, window=5)
model.wv.add_vectors(kv.index_to_key, kv.vectors)

#새 데이터 탑재
model.build_vocab(keywords, update = True)
model2 = gensim.models.Word2Vec(keywords, vector_size=200, min_count=1, negative=5, window=5)
model.train(keywords, total_examples=202304, epochs=10)
print(model.wv.vectors.shape)

model.save('ko_with_corpus_mc1.model')