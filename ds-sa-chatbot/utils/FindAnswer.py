import json

class FindAnswer:
    def __init__(self, db):
        self.db = db
        with open('train_tools/qna/faq.json', 'r', encoding='utf-8') as f:
            self.faq=json.load(f)
        with open('train_tools/qna/branch.json', 'r', encoding='utf-8') as br:
            self.branch=json.load(br)

    # 검색 쿼리 생성
    def _make_query(self, intent_name, ner_predicts):
        sql = "select * from chatbot_train_data"
        if intent_name != None and ner_predicts == None:
            sql = sql + " where intent='{}' ".format(intent_name)

        elif intent_name != None and ner_predicts != None:
            where = ' where intent="%s" ' % intent_name
            if (len(ner_predicts) > 0):
                where += 'and ('
                for word, ne in ner_predicts:
                    if ne!='O': #'O'인 경우는 제외
                        where += " ner like '%{}%' or ".format(ne)
                where = where[:-3] + ')'
            sql = sql + where

        # 동일한 답변이 2개 이상인 경우, 랜덤으로 선택
        sql = sql + " order by rand() limit 1"
        return sql

    # 답변 검색
    def search2(self, intent_name, ner_predicts):
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(intent_name, ner_predicts)
        answer = self.db.select_one(sql)

        # 검색되는 답변이 없으면 의도명만 검색
        if answer is None:
            sql = self._make_query(intent_name, None)
            answer = self.db.select_one(sql)

        answer_sent=answer['answer']
        #ner tag를 원래 단어로 변환
        for word, tag in ner_predicts:

            # 변환해야하는 태그가 있는 경우 추가
            if tag == 'B_FOOD':
                answer_sent = answer_sent.replace(tag, word)

        answer_sent = answer_sent.replace('{', '')
        answer_sent = answer_sent.replace('}', '')

        return (answer_sent, answer['answer_code'])
    
    # 답변 검색
    def search(self, intent_name, ner_predicts):
        answer=None
        answer_code=None

        if intent_name=="인사":
            answer="네 안녕하세요 :D\n반갑습니다. 온더보더입니다."
        if intent_name=="예약":
            answer_code='1'
        if intent_name=="주문취소":
            answer_code='11'
        if intent_name=="주문":
            answer_code='2'
            for word, tag in ner_predicts:
                if tag=="B_FOOD":
                    answer_code='12'
        if intent_name=="메뉴추천":
            answer_code='3'
        if intent_name=="메뉴안내":
            answer_code='3'
            for word, tag in ner_predicts:
                if word=="뭐":
                    answer_code='4'
        if intent_name=="매장문의" or intent_name=="매장정보":
            answer_code='4'
        if intent_name=="이벤트정보":
            answer_code='5'

        return (answer, answer_code)
    
    #지점 faq 답 생성
    def make_sentence(self, exactname, info, keytag):
        if keytag=="parking":
            answer=f"{info}"
        if keytag=="transportation":
            answer=f"{info}"
        if keytag=="location":
            answer=f"{exactname}점의 주소는 {info}입니다."
        if keytag=="phone":
            answer=f"{exactname}점의 전화번호는 {info}입니다."
        if keytag=="time":
            answer=f"{exactname}점의 영업시간은 {info}입니다."
        return answer


    #faq 답 생성
    def match_answer(self, tagword, intent, ner_predicts):
        if intent=="매장정보":
            answer="매장별 번호, 주차, 교통, 위치 등 기본 정보는 홈페이지의 매장 탭에 안내되어있으니 참고 부탁드립니다." #기본 메시지
            if tagword in ["주차", "주차장"]: 
                keytag="parking"
            elif tagword in ["교통"]: 
                keytag="transportation"
            elif tagword in ["주소", "위치"]: 
                keytag="location"
            elif tagword in ["전화", "번호", "전화번호"]: 
                keytag="phone"
            elif tagword in ["이용시간"]: 
                keytag="time"

            for word, tag in ner_predicts:
                for brch in self.branch:
                    if word in brch["name"]:
                        exactname=brch['exactname']
                        info=brch[keytag]
            answer=self.make_sentence(exactname, info, keytag)

        if intent=="매장문의":
            answer = "상담원 연결을 도와드리겠습니다. 잠시만 기다려주세요." #기본 메시지
            if tagword in self.faq.keys():
                answer=self.faq[tagword]
            else:
                for word in self.faq.keys():
                    if tagword in word:
                        answer=self.faq[word]

        return answer
    

    def abb_menu(self, tagword, menu):
        mod_menu={}
        for cat_name, cat_list in menu.items():
            for food in cat_list:
                if tagword in cat_list['rec_cat']:
                    if cat_name in mod_menu.keys():
                        mod_menu[cat_name].append(food)
                    else:
                        mod_menu[cat_name]=[food]
        return mod_menu


    def show_menu(self, tagword, menu):
        wordtonum={ "두":"2", "세":"3", "네":"4","다섯":"5","여섯":"6","일곱":"7","여덟":"8","아홉":"9","열":"10"}
        if tagword in wordtonum.keys():
            tagword=wordtonum[tagword]
        if tagword==None:
            #전체
            mod_menu=menu
            answer="전체 메뉴판을 준비해드리겠습니다."
        elif tagword in ["2","3","4","5","6","7","8","9","10"]:
            #인원
            mod_menu=self.abb_menu(tagword, menu)     
            answer=f"{tagword}명 추천 메뉴는 다음과 같이 준비되어있습니다."
        elif tagword in ["키즈", "가족", "커플", "혼밥", "비건", "베지테리언", "채식", "어린이"]:
            #태그
            mod_menu=self.abb_menu(tagword, menu)     
            answer=f"{tagword} 추천 메뉴는 다음과 같이 준비되어있습니다."
            if tagword in ["비건", "베지테리언", "채식"]:
                answer = "해당 메뉴는 기본적으로 비건이 아닙니다. 비건 옵션으로 추가 변경이 필요하므로, 직원에게 문의 부탁드립니다."
        elif tagword in ["라이스", "수프", "스테이크","샐러드","화이타","퀘사디아","타코","부리또","버거","디저트","드링크","음료수"]:
            #카테고리
            mod_menu=self.abb_menu(tagword, menu)     
            answer=f"{tagword}메뉴는 다음과 같이 준비되어있습니다."
        else:
            #아무것도 아니면 기본 추천메뉴
            mod_menu=self.abb_menu("Best", menu)     
            answer=f"온더보더 베스트 메뉴는 다음과 같이 준비되어있습니다."

        return answer, mod_menu
        
