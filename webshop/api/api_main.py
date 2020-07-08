from flask import Flask, Blueprint
from flask_restful import Api
from .resources import *
from ...main import app

app.register_blueprint()

api = Api(app)

api.add_resource(CategoryResource, '/categories', '/categories/<category_id>',
                 '/categories/new', '/categories/new/<parent_id>')
api.add_resource(ProductResource, '/products', '/products/<product_id>', '/products/new')
api.add_resource(UserResource, '/users', '/users/<user_id>', '/users/new')
api.add_resource(TextResource, '/texts', '/texts/<text_id>', '/texts/new')
api.add_resource(OrderResource, '/orders', '/orders/<order_id>', '/orders/new')

categories_blueprint =
products_blueprint =
users_blueprint =
texts_blueprint =
orders_blueprint =

if __name__ == '__main__':
    app.run(debug=True)