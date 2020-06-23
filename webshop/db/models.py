import mongoengine as me
import datetime


me.connect('webshop_db')


class Category(me.Document):

    title = me.StringField(min_length=1, max_length=512)
    description = me.StringField(min_length=2, max_lenght=4096, default=None)
    subcategories = me.ListField(me.ReferenceField('self'))
    parent = me.ReferenceField('self', default=None)

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

    #
    # @property
    # def title(self):
    #     return self.title


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
    in_stock = me.BooleanField(default=True)
    image = me.FileField(required=True)
    category = me.ReferenceField('Category')
    attrs = me.EmbeddedDocumentField(Attrs)

    @property
    def extended_price(self):
        return self.price * (100 - self.discount) / 100

    @classmethod
    def get_discount_products(cls):
        return cls.objects(discount__ne=0, in_stock=True)


class User(me.Document):

    message_chat_id = me.StringField(unique=True)
    name = me.StringField()
    surname = me.StringField()
    status = me.StringField()
    phone = me.StringField()
    address = me.StringField()
    cart = me.ListField(me.ReferenceField(Product))


class Text(me.Document):

    TITLES = {
        'greetings': 'Текст приветствия',
        'cart': 'Текст корзины',
        'categories': 'Текст категории'
    }

    title = me.StringField(min_length=1, max_length=256, choices=TITLES.values(), unique=True)
    body = me.StringField(min_length=1, max_length=4096)
