class FavTb:
    def __init__(self, execute) -> None:
        self.execute = execute

    def add(self, name, tp, value):
        if tp != 'dish':
            value = "'" + value + "'"
        name = "'" + name + "'"
        self.execute(
            f"insert into fav_{tp} (name, {tp}) values({name}, {value})")

    def delete(self, name, tp, value):
        name = "'" + name + "'"
        if tp != 'dish':
            value = "'" + value + "'"
        self.execute(
            f"delete from fav_{tp} where name = {name} and {tp} = {value}")
