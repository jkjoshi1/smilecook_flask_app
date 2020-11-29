from flask import Flask
from flask_restful import Api
from Resources.recipe import RecipeListResource,RecipePublishResource,RecipeResource

app = Flask(__name__)
api = Api(app)

api.add_resource(RecipeListResource, '/recipes')
api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')


if __name__ == "__main__":
    app.run(port=5000, debug=True)

