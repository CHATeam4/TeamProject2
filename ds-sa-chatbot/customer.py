import json

class Customer:
    def __init__(self):
        self.name='김코딩'
        self.phone_num='01012345678'
        self.adr='서울시 강남구'
        self.flag=0 #0: 원격, 1: 매장
        self.bag=[]
        self.numbag={}
        self.reservation=[] #(person, time)꼴로 관리

        with open('menu.json', 'r', encoding='utf-8') as f:
            self.menu=json.load(f)
            self.price={}
            for cat in self.menu.values():
                for food in cat:
                    self.price[food["name"]]=int(food["price"])

    def put_item(self, item, num):
        if item not in self.bag:
            self.bag.append(item)
        
        if item in self.numbag.keys():
            self.numbag[item]+=num
        else:
            self.numbag[item]=num
    
    def cancel_item(self, item):
        self.bag.remove(item)
        self.numbag[item]=0

    def order_item(self):
        self.bag.clear()
        for item in self.numbag.keys():
            self.numbag[item]=0
    
    def charge(self):
        total=0
        for item in self.numbag.keys():
            total+=self.price[item]*self.numbag[item]
        return total
    
    def updateinfo(self, newname, phone):
        self.name=newname
        self.phone_num=phone
   
    def reserv(self, time, person):
        self.reservation.append([time,person])
        self.reservation.sort()

    def cancel_reserv(self, time):
        for reserv in self.reservation:
            if reserv[0]==time:
                self.reservation.remove(reserv)
