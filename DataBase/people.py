from PIL import Image
from io import BytesIO


class PeopleTb:
    def __init__(self, execute) -> None:
        self.execute = execute

    def sign_in(self, name, passwd):
        return len(self.execute(f"select * from people where name = '{name}' and passwd = '{passwd}';")) != 0

    def sign_up(self, name, nick, passwd):
        name = "'" + name + "'"
        exist = self.execute(f'select * from people where name = {name};')
        if len(exist) > 0:
            return False
        self.execute(
            f"insert into people (name, nick, passwd, sex, birth, fav, ates) values ({name}, '{nick}', '{passwd}', 0, '', 0, 0);")
        return True

    def update(self, name, field, value):
        if field in ['nick', 'passwd', 'birth']:
            value = "'" + value + "'"
        if field == 'photo':
            with open(value, 'rb') as f:
                value = f.read()
            query = 'update people set photo = %s where name = %s'
            self.execute(query, (value, name))
        else:
            self.execute(
                f"update people set {field} = {value} where name = '{name}';")

    def get(self, name):
        name = "'" + name + "'"
        person = list(self.execute(f'select * from people where name = {name}')[0])
        if person[7] is not None:
            person[7] = Image.open(BytesIO(person[7]))
        else:
            person[7] = None
        return person
