import mongoengine as me
import datetime
from mongoengine import ValidationError
import os
from .seeder import TITLES


me.connect('webshop_db')


class Category(me.Document):

    title = me.StringField(min_length=1, max_length=512)
    description = me.StringField(min_length=2, max_lenght=4096, default='')
    subcategories = me.ListField(me.ReferenceField('self'), default=[])
    parent = me.ReferenceField('self')

    def get_products(self):
        return Product.objects(category=self)

    def add_subcategory(self, category: 'Category'):
        category.parent = self
        category.save()
        self.subcategories.append(category)
        self.save()

    @classmethod
    def get_root_categories(cls):
        return cls.objects(parent=None)

    @classmethod
    def get_subcategories(cls, parent_name):
        parent = cls.objects.get(title=parent_name)
        return cls.objects(parent=parent)

    @property
    def is_parent(self):
        return bool(self.subcategories)

    @property
    def has_parent(self):
        return bool(self.parent)

    @classmethod
    def create(cls, parent_obj, **kwargs):
        data = dict(**kwargs)
        if parent_obj:
            data['parent'] = parent_obj
        return cls.objects.create(**data)

    @classmethod
    def read(cls, category_id):
        try:
            obj = cls.objects.get(id=category_id)
        except ValidationError:
            obj = None
        return obj

    @classmethod
    def update(cls, category_id, **kwargs):

        category_obj = Category.objects.get(id=category_id)

        if 'title' in kwargs.keys():
            category_obj.title = kwargs['title']
        if 'description' in kwargs.keys():
            category_obj.description = kwargs['description']
        if 'parent' in kwargs.keys():
            parent = Category.objects.get(id=kwargs['parent'])
            category_obj.parent = parent
        if 'add_subcategories' in kwargs.keys():
            for _id in kwargs['add_subcategories']:
                subcategory = Category.objects.get(id=_id)
                if subcategory in category_obj.subcategories:
                    pass
                else:
                    category_obj.subcategories.append(subcategory)
        if 'del_subcategories' in kwargs.keys():
            for _id in kwargs['del_subcategories']:
                subcategory = Category.objects.get(id=_id)
                category_obj.subcategories.remove(subcategory)
        category_obj.save()
        return category_obj

    @classmethod
    def delete(cls, category_id):
        cls.objects(id=category_id).delete()


class Attrs(me.EmbeddedDocument):

    height = me.FloatField()
    length = me.FloatField()
    width = me.FloatField()
    weight = me.FloatField()


class Product(me.Document):

    title = me.StringField(min_length=1, max_length=512)
    description = me.StringField(min_length=2, max_length=4096)
    created = me.DateTimeField(default=datetime.datetime.now())
    price = me.DecimalField(required=True)
    discount = me.IntField(min_value=0, max_value=100, default=0)
    in_stock = me.IntField(default=1)
    image = me.FileField(required=False)
    category = me.ReferenceField('Category')
    attrs = me.EmbeddedDocumentField(Attrs)

    @property
    def extended_price(self):
        return self.price * (100 - self.discount) / 100

    @classmethod
    def get_discount_products(cls):
        return cls.objects(discount__ne=0, in_stock__ne=0)

    @classmethod
    def create(cls, **kwargs):
        data = dict(**kwargs)
        image_name = data.pop('image_name')
        data['category'] = Category.objects.get(id=kwargs['category_id'])
        del data['category_id']
        product = cls.objects.create(**data)

        path = os.path.abspath('../db/pics/' + image_name + '.jpg')
        with open(path, 'rb') as picture:
            product.image.replace(picture, content_type='image/jpg')
            product.save()

        return product

    @classmethod
    def read(cls, product_id):
        try:
            obj = cls.objects.get(id=product_id)
        except ValidationError:
            obj = None
        return obj

    @classmethod
    def update(cls, product_id, **kwargs):

        product_obj = Product.objects.get(id=product_id)

        if 'title' in kwargs.keys():
            product_obj.title = kwargs['title']
        if 'description' in kwargs.keys():
            product_obj.description = kwargs['description']
        if 'price' in kwargs.keys():
            product_obj.price = kwargs['price']
        if 'discount' in kwargs.keys():
            product_obj.discount = kwargs['discount']
        if 'in_stock' in kwargs.keys():
            product_obj.in_stock = kwargs['in_stock']
        if 'attrs' in kwargs.keys():
            attrs = kwargs['attrs']
            if 'height' in attrs.keys():
                product_obj.attrs.height = attrs['height']
            if 'length' in attrs.keys():
                product_obj.attrs.length = attrs['length']
            if 'width' in attrs.keys():
                product_obj.attrs.width = attrs['width']
            if 'weight' in attrs.keys():
                product_obj.attrs.weight = attrs['weight']
        if 'category_id' in kwargs.keys():
            category = Category.objects.get(id=kwargs['category_id'])
            product_obj.category = category
        if 'image_name' in kwargs.keys():
            path = os.path.abspath('../db/pics/' + kwargs['image_name'] + '.jpg')
            with open(path, 'rb') as picture:
                product_obj.image.replace(picture, content_type='image/jpg')

        product_obj.save()
        return product_obj

    @classmethod
    def delete(cls, product_id):
        cls.objects(id=product_id).delete()


class User(me.Document):

    message_chat_id = me.StringField(unique=True)
    name = me.StringField()
    surname = me.StringField()
    status = me.StringField()
    phone = me.StringField()
    address = me.StringField()
    cart = me.ListField(me.ReferenceField('Product'))
    cart_total_message_id = me.StringField()

    def add_to_cart(self, product):
        self.cart.append(product)
        self.save()

    def save_phone(self, phone_number):
        self.phone = phone_number
        self.save()

    def plus_cart(self, product):
        self.cart.append(product)
        self.save()

    def minus_cart(self, product):
        self.cart.remove(product)
        self.save()

    def empty_cart(self):
        self.cart = []
        self.save()

    def remove_from_cart(self, product):
        self.cart[:] = (prod for prod in self.cart if prod != product)
        self.save()

    def set_total_message_id(self, message_id):
        self.cart_total_message_id = message_id
        self.save()

    @property
    def total_message_chat_id(self):
        return self.cart_total_message_id

    @property
    def cart_total(self):
        def total_sum(cart_list):
            if len(cart_list) == 0:
                return 0
            elif len(cart_list) == 1:
                return cart_list[0].extended_price
            else:
                return cart_list[0].extended_price + total_sum(cart_list[1:])
        return total_sum(self.cart)

    @classmethod
    def get_user(cls, message_chat_id):
        return cls.objects.get(message_chat_id=message_chat_id)

    @classmethod
    def create(cls, **kwargs):
        return cls.objects.create(**kwargs)

    @classmethod
    def read(cls, user_id):
        try:
            obj = cls.objects.get(id=user_id)
        except ValidationError:
            obj = None
        return obj

    @classmethod
    def update(cls, user_id, **kwargs):

        user_obj = User.objects.get(id=user_id)

        if 'message_chat_id' in kwargs.keys():
            user_obj.message_chat_id = kwargs['message_chat_id']
        if 'name' in kwargs.keys():
            user_obj.name = kwargs['name']
        if 'surname' in kwargs.keys():
            user_obj.surname = kwargs['surname']
        if 'status' in kwargs.keys():
            user_obj.status = kwargs['status']
        if 'phone' in kwargs.keys():
            user_obj.phone = kwargs['phone']
        if 'address' in kwargs.keys():
            user_obj.address = kwargs['address']
        if 'add_to_cart' in kwargs.keys():
            for _id in kwargs['add_to_cart']:
                product = Product.objects.get(id=_id)
                user_obj.plus_cart(product)
        if 'del_from_cart' in kwargs.keys():
            for _id in kwargs['del_from_cart']:
                product = Product.objects.get(id=_id)
                user_obj.minus_cart(product)

        user_obj.save()
        return user_obj

    @classmethod
    def delete(cls, user_id):
        cls.objects(id=user_id).delete()


class Order(me.Document):

    user = me.ReferenceField('User')
    phone = me.StringField()
    time_stamp = me.DateTimeField()
    products = me.ListField(me.ReferenceField('Product'))

    @classmethod
    def place_order(cls, user):
        Order.objects.create(user=user, phone=user.phone, products=user.cart)

    def plus_order(self, product):
        self.products.append(product)
        self.save()

    def minus_order(self, product):
        self.products.pop(product)
        self.save()

    @classmethod
    def create(cls, **kwargs):
        return cls.objects.create(**kwargs)

    @classmethod
    def read(cls, order_id):
        try:
            obj = cls.objects.get(id=order_id)
        except ValidationError:
            obj = None
        return obj

    @classmethod
    def update(cls, order_id, **kwargs):

        order_obj = Order.objects.get(id=order_id)

        if 'user' in kwargs.keys():
            order_obj.user = kwargs['user']
        if 'phone' in kwargs.keys():
            order_obj.phone = kwargs['phone']
        if 'add_to_order' in kwargs.keys():
            for _id in kwargs['add_to_order']:
                product = Product.objects.get(id=_id)
                order_obj.plus_order(product)
        if 'del_from_order' in kwargs.keys():
            for _id in kwargs['del_from_order']:
                product = Product.objects.get(id=_id)
                order_obj.minus_order(product)
        order_obj.save()
        return order_obj

    @classmethod
    def delete(cls, order_id):
        cls.objects(id=order_id).delete()


class Text(me.Document):

    title = me.StringField(min_length=1, max_length=256, choices=TITLES.keys(), unique=True)
    body = me.StringField(min_length=1, max_length=4096)

    @classmethod
    def get_text(cls, title):
        body = Text.objects.get(title=title).body
        return body

    @classmethod
    def create(cls, **kwargs):
        cls.objects.create(**kwargs)

    @classmethod
    def read(cls, text_id):
        try:
            obj = cls.objects.get(id=text_id)
        except ValidationError:
            obj = None
        return obj

    @classmethod
    def update(cls, text_id, **kwargs):

        text_obj = Text.objects.get(id=text_id)

        if 'title' in kwargs.keys():
            text_obj.title = kwargs['title']
        if 'body' in kwargs.keys():
            text_obj.body = kwargs['body']

        text_obj.save()
        return text_obj

    @classmethod
    def delete(cls, text_id):
        cls.objects(id=text_id).delete()
