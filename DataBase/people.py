class PeopleTb:
    def __init__(self, execute) -> None:
        self.execute = execute

    def sign_in(self, name, passwd):
        return len(self.execute(f"select * from people where name = '{name}' and passwd = '{passwd}';")) != 0

    def sign_up(self, name, nick, passwd):
        self.execute(
            f"insert into people (name, nick, passwd, sex, birth, fav, ates) values ('{name}', '{nick}', '{passwd}', 0, '', 0, 0);")

    def update(self, name, field, value):
        if field in ['nick', 'passwd', 'birth']:
            value = "'" + value + "'"
        self.execute(
            f"update people set {field} = {value} where name = '{name}';")
