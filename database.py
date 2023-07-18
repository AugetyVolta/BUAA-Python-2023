import pymysql


class DBOperator:
    def __init__(self) -> None:
        self.db = pymysql.connect(host='39.105.140.212',
                                  user='remote_user',
                                  port=3306,
                                  password='1Qa2Ws3Ed',
                                  database='canteen')
        self.cursor = self.db.cursor()

    def __wrap__(self, sql: str) -> tuple:
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()

    def disconnect(self) -> None:  # 断开数据库连接的操作，需要在最后执行一次
        self.db.close()

    def get_line_num(self, table: str) -> int:
        sql = f'select count(*) from {table};'
        return self.__wrap__(sql)[0][0]

    # 获取名为name的菜，由于菜可以重名，返回的是包含多个tuple的tuple
    # 形如((名称，类型，冷热，口味，柜台，大厅，次数), ...)
    def get_dish(self, name: str, bar: str, hall: str) -> tuple[tuple[str, int, int, int, str, str, int], ...]:
        sql = f"SELECT * FROM dishes WHERE name = '{name}' AND bar = '{bar}' AND hall = '{hall}';"
        return self.__wrap__(sql)

    def insert_dish(self, name: str, tp: int, heat: int, taste: int, bar: str, hall: str, times: int) -> None:
        sql = f"INSERT INTO dishes (name, tp, heat, taste, bar, hall, times) " \
              f"VALUES ('{name}', {tp}, {heat}, {taste}, '{bar}', '{hall}', {times});"
        self.__wrap__(sql)

    def delete_dish(self, name: str, bar: str, hall: str) -> None:
        sql = f"DELETE FROM dishes WHERE name = '{name}' AND bar = '{bar}' AND hall = '{hall}';"
        self.__wrap__(sql)

    def change_dish(self, name: str, tp: int, heat: int, taste: int, bar: str, hall: str, times: int) -> None:
        self.delete_dish(name, bar, hall)
        self.insert_dish(name, tp, heat, taste, bar, hall, times)

    def sign_in(self, user_id: int) -> bool:
        sql = f"SELECT * FROM users WHERE id = {user_id};"
        return len(self.__wrap__(sql)) == 0

    def sign_up(self, user_id: int, name: str) -> None:
        sql = f"INSERT INTO users (id, name, fd, fb, fh, ate) VALUES ({user_id}, '{name}', '', '', '', '');"
        self.__wrap__(sql)

    def add_ate(self, user_id: int, dish_name: str, bar: str, hall: str) -> None:
        dish_str = dish_name + '-' + bar + '-' + hall + ','
        sql = f"select ate from users where id = {user_id};"
        self.__wrap__(sql)
        ate = cursor.fetchone()[0] + dish_str
        sql = f"update users set ate = '{ate}' where id = {user_id};"
        self.__wrap__(sql)

    def change_fd(self, user_id: int, dish_name: str, bar: str, hall: str, add=True) -> None:
        dish_str = dish_name + '-' + bar + '-' + hall + ','
        sql = f"select fd from users where id = {user_id};"
        self.__wrap__(sql)
        if add:
            fd = cursor.fetchone()[0] + dish_str
        else:
            fd = cursor.fetchone()[0].replace(dish_str, '')
        sql = f"update users set fd = '{fd}' where id = {user_id};"
        self.__wrap__(sql)

    def change_fb(self, user_id: int, bar: str, hall: str, add=True) -> None:
        bar_str = bar + '-' + hall + ','
        sql = f"select fb from users where id = {user_id};"
        self.__wrap__(sql)
        if add:
            fb = cursor.fetchone()[0] + bar_str
        else:
            fb = cursor.fetchone()[0].replace(bar_str, '')
        sql = f"update users set fb = '{fb}' where id = {user_id};"
        self.__wrap__(sql)

    def change_fh(self, user_id: int, hall: str, add=True) -> None:
        hall_str = hall + ','
        sql = f"select fh from users where id = {user_id};"
        self.__wrap__(sql)
        if add:
            fh = cursor.fetchone()[0] + hall_str
        else:
            fh = cursor.fetchone()[0].replace(hall_str, '')
        sql = f"update users set fh = '{fh}' where id = {user_id}"
        self.__wrap__(sql)

    def get_ates(self, user_id: int) -> list[list[str, str, str], ...]:
        sql = f"select ate from users where id = {user_id};"
        ates = self.__wrap__(sql)[0][0].split(',')[:-1]
        return [dish.split('-') for dish in ates]

    def get_fd(self, user_id: int) -> list[list[str, str, str], ...]:
        sql = f"select fd from users where id = {user_id};"
        fds = self.__wrap__(sql)[0][0].split(',')[:-1]
        return [dish.split('-') for dish in fds]

    def get_fb(self, user_id: int) -> list[list[str, str], ...]:
        sql = f"select fb from users where id = {user_id}"
        fbs = self.__wrap__(sql)[0][0].split(',')[:-1]
        return [bar.split('-') for bar in fbs]

    def get_fh(self, user_id: int) -> list[str]:
        sql = f"select fh from users where id = {user_id}"
        return self.__wrap__(sql)[0][0].split(',')[:-1]


if __name__ == '__main__':
    op = DBOperator()
    a = op.get_line_num('users')
    print(a, type(a))
    op.disconnect()
