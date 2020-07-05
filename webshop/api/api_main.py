from flask import Flask
from flask_restful import Api
from .resources import *


api_app = Flask(__name__)
api = Api(api_app)

api.add_resource(CategoryResource, '/categories', '/categories/<category_id>',
                 '/categories/new', '/categories/new/<parent_id>')
api.add_resource(ProductResource, '/products', '/products/<product_id>', '/products/new')
api.add_resource(UserResource, '/users', '/users/<user_id>', '/users/new')
api.add_resource(TextResource, '/texts', '/texts/<text_id>', '/texts/new')


if __name__ == '__main__':
    app.run(debug=True)