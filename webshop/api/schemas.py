from marshmallow import Schema, fields, ValidationError, validate


class CategorySchema(Schema):

    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=512))
    description = fields.String(required=True, validate=validate.Length(min=1, max=4096))
    subcategories = fields.List(fields.Nested(lambda: CategorySchema), dump_only=True)
    parent = fields.Nested(lambda: CategorySchema(only=("id", "title")), dump_only=True)


class BinaryField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, bytes):
            raise ValidationError('Image should be in binary format')


class AttrsSchema(Schema):

    height = fields.Float()
    length = fields.Float()
    width = fields.Float()
    weight = fields.Float()

    # def _validate(self, value):
    #     for attr in value.values():
    #         if not isinstance(attr, float):
    #             raise ValidationError('Attributes should be in float format')


class ProductSchema(Schema):

    id = fields.String(dump_only=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    created = fields.Date(required=False)
    price = fields.Float(required=True)
    discount = fields.Float(default=None)
    in_stock = fields.Integer(default=1, validate=validate.Range(min=0, max=1))
    category = fields.Nested(CategorySchema, dump_only=True)
    attrs = fields.Nested(AttrsSchema)

    category_id = fields.String(load_only=True)
    image_name = fields.String(load_only=True)


class UserSchema(Schema):

    id = fields.String(dump_only=True)
    message_chat_id = fields.String(dump_only=True)
    name = fields.String()
    surname = fields.String()
    status = fields.String()
    phone = fields.String()
    address = fields.String()
    cart = fields.List(fields.Nested(lambda: ProductSchema(only=("id", "title"))), dump_only=True)
    cart_total_message_id = fields.String(load_only=True)


class OrderSchema(Schema):

    id = fields.String(dump_only=True)
    user = fields.Nested(lambda: UserSchema(only=("phone", "name", "surname", "address")))
    phone = fields.String()
    timestamp = fields.DateTime(dump_only=True)
    products = fields.List(fields.Nested(lambda: ProductSchema(only=("id", "title"))))


class TextSchema(Schema):

    id = fields.String(dump_only=True)
    title = fields.String()
    body = fields.String()
