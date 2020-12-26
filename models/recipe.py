from extensions import db
recipe_list = []


def get_last_id():
    if recipe_list:
        last_recipe = recipe_list[-1]
    else:
        return 1

    return last_recipe.id+1


class Recipe(db.Model):

    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(200))
    no_of_serving = db.Column(db.Integer, nullable=False)
    cook_time = db.Column(db.Integer)
    direction = db.Column(db.String(1000))
    is_publish = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __init__(self, name, description, no_of_serving, cook_time, direction, user_id):
        #self.id = get_last_id()
        self.name = name
        self.description = description
        self.no_of_serving = no_of_serving
        self.cook_time = cook_time
        self.direction = direction
        self.is_publish = False
        self.user_id = user_id

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

