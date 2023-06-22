#model = gensim.models.Word2Vec.load('ko/ko.bin')
#model = gensim.models.KeyedVectors.load_word2vec_format('ko/ko.bin', encoding='utf8')
#Pretrained W2V: https://github.com/Kyubyong/wordvectors

#https://drive.google.com/file/d/1ZiDi_xvqzUvmf7MqLn4AgB9VRQ5rPKRd/view?usp=drive_link

import pandas as pd
import gensim
import numpy as np
import csv
import re

from utils.PreprocessW2V import PreprocessW2V
from utils.Preprocess import Preprocess

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import preprocessing
from sklearn.model_selection import train_test_split
import numpy as np

from utils.PreprocessW2V import PreprocessW2V as Preprocess
from models.ner.NerModel_New import NerModel
#from models.intent.IntentModel import IntentModel
from models.intent.IntentModel_New import IntentModel


# 전처리 객체 생성
p = Preprocess(w2v_model='ko_with_corpus_mc1_menu_added.kv', userdic='utils/user_dic.txt')

# 의도 파악 모델
#intent = IntentModel(model_name='models/intent/intent_w2v_model.h5', proprocess=p)
intent = IntentModel(proprocess=p)

# 개체명 인식 모델
ner = NerModel(proprocess=p)

# 학습 파일 불러오기
def read_file(file_name):
    sents = []
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for idx, l in enumerate(lines):
            if l[0] == ';' and lines[idx + 1][0] == '$':
                this_sent = []
            elif l[0] == '$' and lines[idx - 1][0] == ';':
                continue
            elif l[0] == '\n':
                sents.append(this_sent)
            else:
                this_sent.append(tuple(l.split()))
    return sents



def compare_dict():
    pw = PreprocessW2V(w2v_model='ko_with_corpus_mc1_menu_added.kv',userdic='utils/user_dic.txt')
    pn = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
               userdic='utils/user_dic.txt')
    cnt=0
    for word in pn.word_index.keys():
        if word not in pw.word_index.keys():
            cnt+=1
    print('words only in basecode corpus:', cnt)

    cnt=0
    for word in pw.word_index.keys():
        if word not in pn.word_index.keys():
            cnt+=1
    print('words only in new corpus:', cnt)

#model = gensim.models.keyedvectors.KeyedVectors.load('ko.kv')
#model = gensim.models.Word2Vec.load('ko_with_corpus_mc1.model')

#print(model.wv.index_to_key) #keylist
#print(model.wv.key_to_index) #key : index dict 
#print(type(model.wv.key_to_index))
#print(model['하'])

'''
# 학습용 말뭉치 데이터를 불러옴
corpus = read_file('models/ner/'+'ner_train.txt')

# 말뭉치 데이터에서 단어와 BIO 태그만 불러와 학습용 데이터셋 생성
sentences, tags = [], []
for t in corpus:
    tagged_sentence = []
    sentence, bio_tag = [], []
    for w in t:
        tagged_sentence.append((w[1], w[3]))
        sentence.append(w[1])
        bio_tag.append(w[3])
    
    sentences.append(sentence)
    tags.append(bio_tag)



#######################
#samples= '타코 부리또 퀘사디아 온더보더 멕시코'
samples='타코랑 부리또 주문할게'
print(ner.predict(samples))
samples='짜장면 짬뽕 바나나 가락지빵 쀍'
print(ner.predict(samples))
samples='짬뽕 짜장면 바나나 가락지빵 쀍'
print(ner.predict(samples))
samples='가락지빵 짬뽕 짜장면 바나나 쀍'
print(ner.predict(samples))
'''

def intent_test():
    train_file = "total_train_data_new.csv"
    data = pd.read_csv('models/intent/'+train_file, delimiter=',')
    queries = data['query'].tolist()
    intents = data['intent'].tolist()
    labels = {0: "인사", 1: "메뉴안내", 2: "주문", 3: "예약", 4: "기타", 5: "메뉴추천", 6: "매장문의", 7: "이벤트정보", 8: "매장정보"}


    f = open('false_note.csv', 'w')
    writer = csv.writer(f)
    cnt=0
    i=0

    for i in range(data.shape[0]):
        
        result=intent.predict_class(queries[i])
        if intents[i] not in labels.keys():
            print(queries[i])
        if result!=labels[intents[i]]:
            cnt+=1
            pos = p.pos(queries[i])
            keywords = p.get_keywords(pos, without_tag=True)
            writer.writerow([queries[i],intents[i], keywords, result])
        i+=1
        
    f.close()
    print('result:',cnt,'per',data.shape[0], '=',1 - cnt/data.shape[0])

def ner_test():
    print(p.pos("부리또 주문할게요"))
    print(ner.predict("부리또 주문할게요"))

intent_test()
#ner_test()