from io import BytesIO
from PIL import Image


class DishesTb:
    def __init__(self, execute) -> None:
        self.execute = execute

    def get(self, dish_id):
        dish = list(self.execute(
            f'select * from dishes where id = {dish_id};')[0])
        dish[8] = Image.open(BytesIO(dish[8]))
        return dish

    def delete(self, dish_id):
        self.execute(f"delete from dishes where id = {dish_id};")
        self.execute(f'update mapper set valid = 0 where id = {dish_id};')

    def add(self, name, tp, heat, taste, bar, hall, img):
        dish_id = self.execute(f'select count(*) from mapper;')[0][0]
        self.execute(f'insert into mapper (id, valid) values({dish_id}, 1);')
        with open(img, 'rb') as f:
            image = f.read()
        query = "insert into dishes (id, name, tp, heat, taste, bar, hall, img) values (%s, %s, %s, %s, %s, %s, %s, %s);"
        self.execute(query, (dish_id, name, tp, heat, taste, bar, hall, image))

    def update(self, dish_id, field, value):
        if field in ['name', 'bar', 'hall', 'com']:
            value = "'" + value + "'"
        if field == 'img':
            with open(value, 'rb') as f:
                value = f.read()
            query = 'update dishes set img = %s where id = %s'
            self.execute(query, (value, dish_id))
        else:
            self.execute(
                f"update dishes set {field} = {value} where id = {dish_id};")
