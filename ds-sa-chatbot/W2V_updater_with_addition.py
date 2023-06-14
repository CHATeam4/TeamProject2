#W2V모델의 원리를 이용, 단어를 직접 추가하

# 필요한 모듈 임포트
import csv
import numpy as np
import gensim
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate
import os

def softmax(a):
    exp_a=np.exp(a)
    sum_exp_a=np.sum(exp_a)
    if sum_exp_a==0:
        sum_exp_a=1
    y=exp_a/sum_exp_a
    return y

#kv=gensim.models.keyedvectors.KeyedVectors.load('ko.kv')
md = gensim.models.Word2Vec.load('ko_with_corpus_mc1.model')
kv=md.wv

# 데이터 읽어오기
train_file = "additional_menu_updater_data.csv"
#트레인 파일 구조: phase;phase를 구분자로 하여, 첫 구간에서는 멕시코와 상관 없는 단어들을 배치, 두번째 구간부터 앞 멕시코와 상관 있는 단어들이 배치됨.
#앞 구간의 단어들이 뒷 구간의 학습에 누적으로 사용됨. 
csvfile=open(train_file, newline='')
rdr = csv.reader(csvfile, delimiter=';')

from utils.PreprocessW2V import PreprocessW2V as Preprocess
p = Preprocess(userdic='utils/user_dic.tsv')

words=[]
vectors=[]
newwords=[]
mode=0 #mode가 0이면 kv 멕시코를 더하지 않음, 1이면 멕시코를 더함. 

for word, sentence in rdr:
    if word=='phase': #중간저장을 통해 여태 학습한 단어를 다음 단어들에 사용 가능하도록 반영, mode변환,
        mode=1
        kv.add_vectors(words, vectors)
        words=[]
        vectors=[]
    else:            
        pos = p.pos(sentence)
        keywords = p.get_keywords(pos, without_tag=True)
        tmp=np.zeros(200)
        keywords=list(set(keywords))
        cnt=0
        for w in keywords:
            if (w!='맥시코') and (w!='O') and (w!=word) and (w in kv.index_to_key):
                tmp+=kv[w]
                cnt+=1
        if cnt==0:
            print('Error:',word)
        if mode==1:
            tmp=softmax(tmp)
            vector=softmax(kv['멕시코']*0.1+tmp)
        else:
            vector=softmax(tmp)
        newwords.append(word) #결과 관찰용 리스트
        words.append(word)
        vectors.append(vector)
kv.add_vectors(words, vectors)
csvfile.close()

#결과 출력(결과 관찰용)
#for word in newwords:
#    print(word, kv.most_similar(word, topn=10))

md.save('ko_with_corpus_mc1_menu_added.model')
print('update complete')