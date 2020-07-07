from flask_restful import Resource
from flask import request
from webshop.db.models import *
from webshop.api.schemas import *
import json


class CategoryResource(Resource):

    def get(self, category_id):
        return json.loads(CategorySchema().dumps(Category.read(category_id=category_id)))

    def post(self, parent_id=None):
        data = json.dumps(request.json)
        if parent_id:
            parent_obj = Category.objects.get(id=parent_id)
        else:
            parent_obj = None
        try:
            data = CategorySchema().loads(data)
            category = Category.create(parent_obj, **data)
            res = json.loads(CategorySchema().dumps(category))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, category_id):
        return json.loads(CategorySchema().dumps(Category.update(category_id, **request.json)))

    def delete(self, category_id):
        Category.delete(category_id)


class ProductResource(Resource):

    def get(self, product_id):
        return json.loads(ProductSchema().dumps(Product.read(product_id)))

    def post(self):
        data = json.dumps(request.json)
        try:
            data = ProductSchema().loads(data)
            product = Product.create(**data)
            res = json.loads(ProductSchema().dumps(product))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, product_id):
        return json.loads(ProductSchema().dumps(Product.update(product_id, **request.json)))

    def delete(self, product_id):
        Product.delete(product_id)


class UserResource(Resource):

    def get(self, user_id):
        return json.loads(UserSchema().dumps(User.read(user_id)))

    def post(self):
        data = json.dumps(request.json)
        try:
            data = UserSchema().loads(data)
            user = User.create(**data)
            res = json.loads(UserSchema().dumps(user))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, user_id):
        return json.loads(UserSchema().dumps(User.update(user_id, **request.json)))

    def delete(self, user_id):
        User.delete(user_id)


class OrderResource(Resource):

    def get(self, order_id):
        return json.loads(OrderSchema().dumps(Order.read(order_id)))

    def post(self):
        data = json.dumps(request.json)
        try:
            data = OrderSchema().loads(data)
            order = Order.create(**data)
            res = json.loads(OrderSchema().dumps(order))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, order_id):
        return json.loads(OrderSchema().dumps(Order.update(order_id, **request.json)))

    def delete(self, order_id):
        User.delete(order_id)


class TextResource(Resource):

    def get(self, text_id):
        return json.loads(TextSchema().dumps(Text.read(text_id)))

    def post(self):
        data = json.dumps(request.json)
        try:
            data = TextSchema().loads(data)
            text = Text.create(**data)
            res = json.loads(TextSchema().dumps(text))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, text_id):
        return json.loads(TextSchema().dumps(Text.update(text_id, **request.json)))

    def delete(self, text_id):
        Text.delete(text_id)
