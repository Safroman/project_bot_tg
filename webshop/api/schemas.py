from marshmallow import Schema, fields, validate


class CategorySchema(Schema):

    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=512))
    description = fields.String(required=True, validate=validate.Length(min=1, max=4096))
    subcategories = fields.List(fields.Nested(lambda: CategorySchema), dump_only=True)
    parent = fields.Nested(lambda: CategorySchema(only=("id", "title")), dump_only=True)

    parent_id = fields.String(load_only=True)
    subcategories_id = fields.List(fields.String(), dump_only=True)


class AttrsSchema(Schema):

    height = fields.Float(validate=validate.Range(min=0))
    length = fields.Float(validate=validate.Range(min=0))
    width = fields.Float(validate=validate.Range(min=0))
    weight = fields.Float(validate=validate.Range(min=0))


class ProductSchema(Schema):

    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=512))
    description = fields.String(required=True, validate=validate.Length(min=1, max=4096))
    created = fields.Date(required=False, dump_only=True)
    price = fields.Float(required=True, validate=validate.Range(min=0))
    discount = fields.Float(default=None, validate=validate.Range(min=0, max=100))
    in_stock = fields.Integer(default=1, validate=validate.OneOf([0, 1]))
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
    user = fields.Nested(lambda: UserSchema(only=("phone", "name", "surname", "address")), dump_only=True)
    phone = fields.String()
    timestamp = fields.DateTime(dump_only=True)
    products = fields.List(fields.Nested(lambda: ProductSchema(only=("id", "title"))))


class TextSchema(Schema):

    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=256))
    body = fields.String(required=True, validate=validate.Length(min=1, max=4096))
