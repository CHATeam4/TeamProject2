import csv
import json
import re


def dic_updater():
    with open("ds-sa-chatbot-priv/chatbot/ds-sa-chatbot/utils/user_dic.txt", 'a') as uf:
        ud=csv.writer(uf)
        ud.writerow("name"+"	NNG")

    with open("ds-sa-chatbot-priv/chatbot/ds-sa-chatbot/additional_dict.csv", 'a') as af:
        ad=csv.writer(af)
        ad.writerow(["name", "B_FOOD"])


def menu_json_maker():
    with open('ds-sa-chatbot-priv/chatbot/ds-sa-chatbot/menu.csv', 'r') as f:
        mcsv=csv.reader(f, delimiter=';')
        menu={}
        for rows in mcsv:
            if len(rows)!=0:
                row=rows[0]
                ko=re.sub(r"[^가-힣&\s]", "", row).rstrip().lstrip()
                en=re.sub(r"[^a-zA-Z&\s]", "", row).rstrip().lstrip()
                no=re.sub(r"[^0-9]", "", row)
                if ":" in row:
                    menu[ko]=[]
                    current=ko
                else:
                    new={}
                    new["name"]=ko
                    new["eng_name"]=en
                    new["price"]=no
                    new["rec_cat"]=[]
                    new["text"]=""
                    menu[current].append(new)

    with open("ds-sa-chatbot-priv/chatbot/ds-sa-chatbot/menu.json", "w", encoding='utf-8') as json_file:
        json.dump(menu, json_file, indent=4, ensure_ascii=False)

menu_json_maker()