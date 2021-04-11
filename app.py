from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from Resources.recipe import RecipeListResource,RecipePublishResource,RecipeResource
from config import Config
from extensions import db, jwt
from models.users import User
from models.recipe import Recipe
from Resources.users import UserListResource, UserResource, MeResource
from Resources.token import TokenResource, RefreshResource, RevokeResource, black_list


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list


def register_resources(app):
    api = Api(app)
    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(TokenResource, '/token')
    api.add_resource(MeResource, '/me')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')


if __name__ == "__main__":
    app = create_app()
    app.run()


