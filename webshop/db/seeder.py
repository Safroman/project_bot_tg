from models import Text, Category, Product, Attrs
from random import randint, choice


# category_titles = ['', '', '', '', '', '']

# categories = {
#     'Продукты': 'Продовольственные товары на любой вкус',
#     'Товары для дома': 'Товары, которые помогут украсить ваш дом',
#     'Электроника': 'Техника для любых целей',
#     'Одежда': 'Все что нужно для вашего стиля',
#     'Спорт и хобби': 'Товары для вашего досуга',
#     'Детские товары': 'Все что нужно детям',
# }

# for key, value in categories.items():
#     Category.objects.create(
#         title=key,
#         description=value
# )

def seed_categories(parent):
    subcats = subcategories[parent.title]
    for cat in subcats:
        Category.objects.create(
            title=cat,
            parent=parent
            )


def put_pics():
    products = Product.objects.filter()
    for product in products:
        file_name = 'pics/' + product.title + '.jpg'
        with open(file_name, 'rb') as picture:
            product.image.replace(picture, content_type='image/jpg')
            product.save()


def seed_attrs():
    products = Product.objects.filter()
    for product in products:
        product.attrs = Attrs(
            height=randint(0, 100),
            length=randint(0, 100),
            width=randint(0, 100),
            weight=randint(0, 100)
        )
        product.save()


if __name__ == '__main__':
    seed_attrs()
