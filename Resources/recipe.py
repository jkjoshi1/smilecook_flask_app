from flask import request
from flask_restful import Resource
from http import HTTPStatus
import sys
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from models.recipe import Recipe
from flask import jsonify


class RecipeListResource(Resource):
    def get(self):
        recipes = Recipe.get_all_published()
        data = []
        for recipe in recipes:
            if recipe.is_publish:
                data.append(recipe.data())

        return {'data': data}, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        recipe = Recipe(
            name=json_data['name'],
            description=json_data['description'],
            no_of_serving=json_data['no_of_serving'],
            cook_time=json_data['cook_time'],
            direction=json_data['direction'],
            user_id=current_user
        )

        recipe.save()
        return recipe.data(), HTTPStatus.CREATED


class RecipeResource(Resource):
    @jwt_optional
    def get(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()

        if recipe.is_publish is False and recipe.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        print(recipe.data, file=sys.stderr)
        return {'data': recipe.data()}, HTTPStatus.OK

    @jwt_required
    def put(self, recipe_id):
        data = request.get_json()
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.description = data['description']
        recipe.no_of_serving = data['no_of_serving']
        recipe.name = data['name']
        recipe.cook_time = data['cook_time']
        recipe.direction = data['direction']

        recipe.save()

        return recipe.data(), HTTPStatus.OK


class RecipePublishResource(Resource):
    @jwt_required
    def put(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.is_publish = True
        recipe.save()
        return jsonify(recipe.data()), HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.delete()
        return {}, HTTPStatus.NO_CONTENT
