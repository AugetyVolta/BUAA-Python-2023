import pymysql

from DataBase.ates import AtesTb
from DataBase.dishes import DishesTb
from DataBase.fav import FavTb
from DataBase.people import PeopleTb
from DataBase.utils import get_recommendation, search_by_name, search_by_adj

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class DBOperator:
    ########## 不需要调用的函数 ##########
    def __init__(self):
        # host = '39.105.140.212'
        # user = 'remote_user'
        host = 'polardb114514.mysql.polardb.rds.aliyuncs.com'
        user = 'temp'
        self.connection = pymysql.connect(host=host,
                                          user=user,
                                          port=3306,
                                          password='1Qa2Ws3Ed',
                                          database='canteen')
        self.cursor = self.connection.cursor()
        self.peopleOp = PeopleTb(self.execute)
        self.atesOp = AtesTb(self.execute)
        self.dishOp = DishesTb(self.execute)
        self.favOp = FavTb(self.execute)
        self.mapping = {
            '温暖': 0b0000_01_00000,
            '凉': 0b0000_10_00000
        }

    def execute(self, query, args=None):
        if args is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, args)
        self.connection.commit()
        return self.cursor.fetchall()

    ######################################

    ########## 菜品表相关函数 ##########

    # 基本的增删改查
    def get_dish(self, dish_id: int):
        return self.dishOp.get(dish_id)

    def add_dish(self, dish: str, tp: int, heat: int, taste: int, bar: str, hall: str, img: str):
        self.dishOp.add(dish, tp, heat, taste, bar, hall, img)

    def del_dish(self, dish_id: int):
        self.dishOp.delete(dish_id)

    def update_dish(self, dish_id, field, value):
        self.dishOp.update(dish_id, field, value)

    # 评论：本质上是用新的评论内容替换原评论内容
    def comment(self, dish_id, content):
        self.update_dish(dish_id, 'com', content)

    # 通过菜品获得id
    def get_id(self, dish, bar, hall):
        return self.dishOp.get_id(dish, bar, hall)

    def get_all_id(self):
        a = self.execute('select id from dishes ;')
        return [i[0] for i in a]

    ########## 已吃表相关函数 ##########
    def get_ates(self, name):
        return self.atesOp.get(name)

    def add_ates(self, name, dish_id, time):
        self.atesOp.add(name, dish_id, time)

    def del_ates(self, name, dish_id, time):
        self.atesOp.delete(name, dish_id, time)

    ###################################

    ########## 人表有关函数 ##########
    def sign_in(self, name, passwd):
        return self.peopleOp.sign_in(name, passwd)

    def sign_up(self, name, nick, passwd):
        return self.peopleOp.sign_up(name, nick, passwd)

    def update_person(self, name, field, value):
        self.peopleOp.update(name, field, value)

    def get_person(self, name):
        return self.peopleOp.get(name)

    ###################################

    ########## 收藏表相关函数 ##########
    def add_fav_dish(self, name, dish):
        self.favOp.add(name, 'dish', dish)
        pre_fav = self.execute(
            f"select fav from people where name = '{name}';")[0][0]

        self.execute(
            f"update people set fav = {pre_fav + 1} where name = '{name}';")

    def del_fav_dish(self, name, dish):
        self.favOp.delete(name, 'dish', dish)
        pre_fav = self.execute(
            f"select fav from people where name = '{name}';")[0][0]

        self.execute(
            f"update people set fav = {pre_fav - 1} where name = '{name}';")

    def get_fav_dish(self, name):
        return self.favOp.get(name, 'dish')

    def add_fav_bar(self, name, bar):
        self.favOp.add(name, 'bar', bar)

    def del_fav_bar(self, name, bar):
        self.favOp.delete(name, 'bar', bar)

    def get_fav_bar(self, name):
        return self.favOp.get(name, 'bar')

    def add_fav_hall(self, name, hall):
        self.favOp.add(name, 'hall', hall)

    def del_fav_hall(self, name, hall):
        self.favOp.delete(name, 'hall', hall)

    def get_fav_hall(self, name):
        return self.favOp.get(name, 'hall')

    ###################################

    ########## 其他函数 ##########
    def recommend(self):
        dishes = self.execute('select * from dishes;')
        ate_record = self.execute('select * from ates;')
        fav_record = self.execute('select * from fav_dish;')
        return get_recommendation(ate_record, fav_record, dishes)

    def get_person_weight(self, name):
        ates = [i[0] for i in self.get_ates(name)]
        ate_dish = [self.get_dish(dish_id) for dish_id in ates]
        ate_weight = np.array([0.0, 0, 0, 0, 0, 0, 0])
        for dish in ate_dish:
            taste = dish[4]
            heat = dish[3]
            ate_weight += np.array(
                [(heat >> 1) & 1, heat & 1, (taste >> 4) & 1, (taste >> 3) & 1, (taste >> 2) & 1, (taste >> 1) & 1,
                 taste & 1])
        ate_weight /= float(len(ates) + 0.000001)
        fav = self.get_fav_dish(name)
        fav_weight = np.array([0.0, 0, 0, 0, 0, 0, 0])
        fav_dish = [self.get_dish(dish_id) for dish_id in fav]
        for dish in fav_dish:
            taste = dish[4]
            heat = dish[3]
            fav_weight += np.array(
                [(heat >> 1) & 1, heat & 1, (taste >> 4) & 1, (taste >> 3) & 1, (taste >> 2) & 1, (taste >> 1) & 1,
                 taste & 1])
        fav_weight /= float(len(fav) + 0.000001)
        return (fav_weight + ate_weight) / 2

    def content_based_recommendation(self, weight, num):
        similarity_scores = {}
        for dish in self.execute('select * from dishes;'):
            taste = dish[4]
            heat = dish[3]
            temp = np.array(
                [(heat >> 1) & 1, heat & 1, (taste >> 4) & 1, (taste >> 3) & 1, (taste >> 2) & 1, (taste >> 1) & 1,
                 taste & 1])
            similarity_scores[dish[0]] = cosine_similarity([weight], [temp])[0][0]
        recommended_dishes = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
        return [i for i, _ in recommended_dishes][:num]

    def collaborative_filtering_recommendation(self, weight, tar_name):
        similar_person = {}
        ates = [i[0] for i in self.get_ates(tar_name)]
        names = [person[0] for person in self.execute('select name from people;')]
        for name in names:
            if name != tar_name:
                similar_person[name] = cosine_similarity([weight], [self.get_person_weight(name)])[0][0]
        recommend_people = [i[0] for i in sorted(similar_person.items(), key=lambda x: x[1], reverse=False)]
        res = []
        for name in recommend_people:
            other_ates = [i[0] for i in self.get_ates(name)]
            for dish_id in other_ates:
                if len(res) > 2:
                    break
                if dish_id not in ates:
                    res.append(dish_id)
        return res

    def personalized_recommendation(self, name):
        weight = self.get_person_weight(name)
        rec1 = self.collaborative_filtering_recommendation(weight, name)
        rec2 = self.content_based_recommendation(weight, 9 - len(rec1))
        return rec2 + rec1

    def search(self, k):
        d = self.execute('select * from dishes;')
        temp = search_by_name(k, d)
        if len(temp) == 0 and k in self.mapping:
            temp = search_by_adj(k, d, self.mapping)
        return temp
    #############################
