import pymysql
from people import PeopleTb
from ates import AtesTb
from dishes import DishesTb


class DBOperator:
    def __init__(self):
        # host = '39.105.140.212'
        # user = 'remote_user'
        host = 'polardb114514.mysql.polardb.rds.aliyuncs.com'
        user = 'temp'
        self.db = pymysql.connect(host=host,
                                  user=user,
                                  port=3306,
                                  password='1Qa2Ws3Ed',
                                  database='canteen')
        self.cursor = self.db.cursor()
        self.peopleOp = PeopleTb(self.execute)
        self.atesOp = AtesTb(self.execute)
        self.dishOp = DishesTb(self.execute)

    def execute(self, sql: str):
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()

    def disconnect(self):  # 断开数据库连接的操作，需要在最后执行一次
        self.db.close()
