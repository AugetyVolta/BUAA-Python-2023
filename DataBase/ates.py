class AtesTb:
    def __init__(self, execute) -> None:
        self.execute = execute

    def add(self, name, dish_id, time):
        self.execute(
            f"insert into ates (name, id, time) values ('{name}', {dish_id}, '{time}');")
        pre_ates = self.execute(
            f"select ates from people where name = '{name}';")[0][0]
        self.execute(
            f"update people set ates = {pre_ates + 1} where name = '{name}';")

    def delete(self, name, dish_id, time):
        self.execute(
            f"delete from ates where name = '{name}' and id = {dish_id} and time = '{time}';")
        pre_ates = self.execute(
            f"select ates from people where name = '{name}';")[0][0]
        self.execute(
            f"update people set ates = {pre_ates - 1} where name = '{name}';")

    def get(self, name):
        return self.execute(f"select * from ates where name = '{name}';")
