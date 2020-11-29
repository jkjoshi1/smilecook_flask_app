recipe_list = []


def get_last_id():
    if recipe_list:
        last_recipe = recipe_list[-1]
    else:
        return 1

    return last_recipe.id


class Recipe:
    def __init__(self, name, description, no_of_serving, cook_time, direction):
        self.id = get_last_id()
        self.name = name
        self.description = description
        self.no_of_serving = no_of_serving
        self.cook_time = cook_time
        self.direction = direction
        self.is_publish = False

    @property
    def data(self):

        return{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'no_of_serving': self.no_of_serving,
            'cook_time': self.cook_time,
            'direction': self.direction,

        }

