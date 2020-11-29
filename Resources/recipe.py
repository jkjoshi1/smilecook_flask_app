from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.recipe import recipe_list, Recipe


class RecipeListResource(Resource):

    def get(self):
        data = []

        for recipe in recipe_list:
            if recipe.is_publish:
                data.append(recipe.data)

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()
        recipe = Recipe(
            name=data['name'],
            description=data['description'],
            no_of_serving=data['no_of_serving'],
            cook_time=data['cook_time'],
            direction=data['direction']
        )

        recipe_list.append(recipe)
        return recipe.data, HTTPStatus.CREATED


class RecipeResource(Resource):

    def get(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id and recipe.is_publish), None)

        if recipe is not None:
            return recipe.data, HTTPStatus.OK
        else:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

    def put(self, recipe_id):
        data = request.get_json()

        recipe = ((recipe for recipe in recipe_list if recipe_id == recipe.id), None)

        if recipe is not None:
            recipe.name = data['name']
            recipe.description = data['description']
            recipe.no_of_serving = data['no_of_serving']
            recipe.cook_time = data['cook_time']
            recipe.direction = data['direction']
        else:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        return recipe.data, HTTPStatus.OK


class RecipePublishResource(Resource):
    def put(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        recipe.is_publish = False

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        recipe.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
