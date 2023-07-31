import datetime
import time
from collections import defaultdict

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
            '早餐': 0b100_00_00000,
            '正餐': 0b010_00_00000,
            '饮料': 0b001_00_00000,
            '温暖': 0b000_01_00000,
            '暖': 0b000_01_00000,
            '热': 0b000_01_00000,
            '凉': 0b000_10_00000,
            '冷': 0b000_10_00000,
            '酸': 0b000_00_10000,
            '甜': 0b000_00_01000,
            '苦': 0b000_00_00100,
            '辣': 0b000_00_00010,
            '咸': 0b000_00_00001,
            '酸辣': 0b000_00_10010,
            '香甜': 0b000_00_01001,
            '微酸': 0b000_00_10000,
            '微苦': 0b000_00_00100,
            '微咸': 0b000_00_00001,
            '浓香': 0b000_01_00000,
            '清淡': 0b000_00_00000,
            '酸甜': 0b000_00_11000,
            '酸苦': 0b000_00_10100,
            '酸咸': 0b000_00_10001,
            '甜苦': 0b000_00_01100,
            '甜辣': 0b000_00_01010,
            '甜咸': 0b000_00_01001,
            '苦辣': 0b000_00_00110,
            '苦咸': 0b000_00_00101,
            '辣咸': 0b000_00_00011,
            '热腾腾': 0b000_01_00000,
            '清凉': 0b000_10_00000,
            '苦涩': 0b000_00_00100,
            '清爽': 0b000_10_00000,
            '酸爽': 0b000_00_10000,
            '香辣': 0b000_00_00010,
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
    
    def update_ates(self, name, dish_id, old_time, new_time):
        self.atesOp.update(name, dish_id, old_time, new_time)

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
    def recommend(self, name=None):
        dishes = self.execute('select * from dishes;')
        ate_record = self.execute('select * from ates;')
        fav_record = self.execute('select * from fav_dish;')
        if name is not None:
            ate_record = [i for i in ate_record if i[0] == name]
            fav_record = [i for i in fav_record if i[0] == name]
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

    def get_time_need(self):
        now = datetime.datetime.now().time()
        time_flag1 = datetime.time(0, 0)
        time_flag2 = datetime.time(10, 0)

        if now >= time_flag1 and now < time_flag2:
            return 0b101
        else:
            return 0b011

    def content_based_recommendation(self, weight, num):
        time_flag = self.get_time_need()
        similarity_scores = {}
        for dish in self.execute('select * from dishes;'):
            taste = dish[4]
            heat = dish[3]
            tp = dish[2]
            if tp & time_flag == 0:
                similarity_scores[dish[0]] = 0
                continue
            temp = np.array(
                [(heat >> 1) & 1, heat & 1, (taste >> 4) & 1, (taste >> 3) & 1, (taste >> 2) & 1, (taste >> 1) & 1,
                 taste & 1])
            similarity_scores[dish[0]] = cosine_similarity([weight], [temp])[0][0]
        recommended_dishes = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
        return [i for i, _ in recommended_dishes][:num]

    def collaborative_filtering_recommendation(self, weight, tar_name):
        time_flag = self.get_time_need()
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
                tp = self.get_dish(dish_id)[2]
                if len(res) > 2:
                    break
                if dish_id not in ates and dish_id not in res and (time_flag & tp != 0):
                    res.append(dish_id)
        return res

    def personalized_recommendation(self, name):
        weight = self.get_person_weight(name)
        rec1 = self.collaborative_filtering_recommendation(weight, name)
        rec2 = self.content_based_recommendation(weight, 100)
        for dish_id in rec2:
            if len(rec1) >= 9:
                break
            if dish_id not in rec1:
                rec1.append(dish_id)
        return rec1

    def get_popularity(self, num):
        ids = [dish[0] for dish in self.execute('select * from dishes;')]
        records = [i[1:] for i in self.execute('select * from ates;')]
        popularity_dict = dict()
        for id in ids:
            popularity_dict[id] = [0, 0]
        current_time = time.time()
        decay_factor = 0.05
        for dish_id, dining_time in records:
            dining_time = dining_time.replace('\n', ' ')
            popularity_dict[dish_id][0] += 1
            dining_timestamp = int(time.mktime(time.strptime(dining_time, "%Y-%m-%d %H:%M:%S")))
            time_difference = current_time - dining_timestamp
            time_weight = pow(decay_factor, time_difference / 1000)
            popularity_dict[dish_id][1] += time_weight
        popularity_result = {}
        for dish_id, (dining_count, time_weight_sum) in popularity_dict.items():
            popularity_score = dining_count * time_weight_sum
            popularity_result[dish_id] = popularity_score
        return sorted(popularity_result.items(), key=lambda x: x[1], reverse=True)[:num]

    def search(self, k):
        d = self.execute('select * from dishes;')
        temp = search_by_name(k, d)
        if len(temp) == 0 and k in self.mapping:
            temp = search_by_adj(k, d, self.mapping)
        if len(temp) == 0:
            return [i[0] for i in self.get_popularity(50)]
        return temp

    #############################

    def get_softmax_weight(self, name):
        taste_weight = self.get_person_weight(name)[2:]
        exp_x = np.exp(taste_weight - np.max(taste_weight))
        return (exp_x / np.sum(exp_x)).tolist()
