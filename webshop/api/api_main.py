from flask import Blueprint
from flask_restful import Api
from .resources import *


api_bp = Blueprint('api', __name__)
admin_api = Api(api_bp)

admin_api.add_resource(CategoryResource, '/categories', '/categories/<category_id>', '/categories/new')
admin_api.add_resource(ProductResource, '/products', '/products/<product_id>', '/products/new')
admin_api.add_resource(UserResource, '/users', '/users/<user_id>', '/users/new')
admin_api.add_resource(TextResource, '/texts', '/texts/<text_id>', '/texts/new')
admin_api.add_resource(OrderResource, '/orders', '/orders/<order_id>', '/orders/new')
