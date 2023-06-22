import json


# NER 태그 사전 불러오기
with open('ds-sa-chatbot-priv/chatbot/ds-sa-chatbot/models/ner/ner2021.json', 'r', encoding='utf-8-sig') as f:
    nerdict = json.load(f)
    #print(json.dumps(self.nerdict) )
    newdict = {}
    for word in nerdict['document']:
        w = word['form']
        l = word['ne'][0]['label']
        newdict[w]=l

##### 추가사전 및 정정 #####
newdict['주문']='O'


with open("ds-sa-chatbot-priv/chatbot/ds-sa-chatbot/models/ner/ner2021_compressed.json", "w") as json_file:
    json.dump(newdict, json_file, indent=4)

print("dictionary size:", len(newdict.keys()))