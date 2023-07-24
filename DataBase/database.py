import pymysql
from people import PeopleTb
from ates import AtesTb
from dishes import DishesTb
from fav import FavTb
from utils import get_recommandation, search_by_adj, search_by_name


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
            '温暖': 0b0000100000,
            '凉': 0
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
        self.peopleOp.sign_in(name, passwd)

    def sign_up(self, name, nick, passwd):
        self.peopleOp.sign_up(name, nick, passwd)

    def update_person(self, name, field, value):
        self.peopleOp.update(name, field, value)
    ###################################

    ########## 收藏表相关函数 ##########
    def add_fav_dish(self, name, dish):
        self.favOp.add(name, 'dish', dish)

    def del_fav_dish(self, name, dish):
        self.favOp.delete(name, 'dish', dish)

    def add_fav_bar(self, name, bar, hall):
        self.favOp.add(name, 'bar', bar + '-' + hall)

    def del_fav_bar(self, name, bar, hall):
        self.favOp.delete(name, 'bar', bar + '-' + hall)

    def add_fav_hall(self, name, hall):
        self.favOp.add(name, 'hall', hall)

    def del_fav_hall(self, name, hall):
        self.favOp.delete(name, 'hall', hall)
    ###################################

    ########## 其他函数 ##########
    def recommand(self):
        ate_record = self.execute('select * from ates;')
        fav_record = self.execute('select * from fav_dish;')
        return get_recommandation(ate_record, fav_record)

    def search(self, k, tp):
        d = self.execute('select * from dishes;')
        if tp == 'name':
            return search_by_name(k, d)
        else:
            return search_by_adj(k, d, self.mapping)
    #############################
