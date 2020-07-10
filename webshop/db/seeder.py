from models import TITLES, Text, Category, Product, Attrs
from random import randint, choice
import mongoengine as me


def init_text(titles):

    for key, value in titles.items():
        Text.objects.create(title=key, body=value)


def init_categories():
    categories = {
        'Продукты': 'Продовольственные товары на любой вкус',
        'Товары для дома': 'Товары, которые помогут украсить ваш дом',
        'Электроника': 'Техника для любых целей',
        'Одежда': 'Все что нужно для вашего стиля',
        'Спорт и хобби': 'Товары для вашего досуга',
        'Детские товары': 'Все что нужно детям',
    }

    for key, value in categories.items():
        Category.objects.create(
            title=key,
            description=value,
            subcategories=[]
        )

    subcategories = {
        "Продукты": ["Фрукты", "Овощи", "Напитки"],
        "Товары для дома": ["Хозяйственные товары", "Мебель", "Декор"],
        "Электроника": ["Кухонная техника", "Бытовая техника", "Компьютеры"],
        "Спорт и хобби": ["Спортивный инвентарь", "Охота", "Рыбалка"],
        "Детские товары": ["Игрушки", "Развивающие", "Детская гигиена"],
        "Одежда": ["Мужская", "Женская", "Детская"],
    }

    def seed_subcategories(parent):
        cats = subcategories[parent.title]
        for cat in cats:
            new_cat = Category.objects.create(
                title=cat,
                description='subcategory description',
                subcategories=[],
                parent=parent)
            parent.add_subcategory(new_cat)

    for category in Category.get_root_categories():
        seed_subcategories(category)


def init_products():
    products = {
        "Фрукты": [
            {"title": "Яблоки",
             "description": "Спелые яблоки"},
            {"title": "Груши",
             "description": "Сочные груши"},
            {"title": "Апельсины",
             "description": "Сладкие апельсины"}
        ],
        "Овощи": [
            {"title": "Картофель",
             "description": "Крупный картофель"},
            {"title": "Морковь",
             "description": "Кладкая морковь"},
            {"title": "Помидоры",
             "description": "Сочные помидоры"}
        ],
        "Напитки": [
            {"title": "Вода",
             "description": "Чистая вода"},
            {"title": "Сок",
             "description": "Полезный сок"},
            {"title": "Пиво",
             "description": "Освежающее пиво"}
        ],
        "Хозяйственные товары": [
            {"title": "Порошок",
             "description": "Лучший порошок"},
            {"title": "Салфетки",
             "description": "Белоснежные салфетки"},
            {"title": "Мыло",
             "description": "Антибактериальное мыло"}
        ],
        "Мебель": [
            {"title": "Стол",
             "description": "Крепкий стол"},
            {"title": "Стул",
             "description": "Удобный стул"},
            {"title": "Шкаф",
             "description": "Вместительный шкаф"}
        ],
        "Декор": [
            {"title": "Шторы",
             "description": "Атласные шторы"},
            {"title": "Ваза",
             "description": "Хрустальная ваза"},
            {"title": "Свеча",
             "description": "Декоративная свеча"}
        ],
        "Кухонная техника": [
            {"title": "Холодильник",
             "description": "Вместительный холодильник"},
            {"title": "Чайник",
             "description": "Быстрый чайник"},
            {"title": "Тостер",
             "description": "Компактный тостер"}
        ],
        "Бытовая техника": [
            {"title": "Телевизор",
             "description": "Широкоформатный телевизор"},
            {"title": "Пылесос",
             "description": "Мощьный пылесос"},
            {"title": "Утюг",
             "description": "Антипригарный утюг"}
        ],
        "Компьютеры": [
            {"title": "Ноутбук",
             "description": "Компактный ноутбук"},
            {"title": "Настольный ПК",
             "description": "Производительный компьютер"},
            {"title": "Игровой компьютер",
             "description": "Мощьный компьютер"}
        ],
        "Спортивный инвентарь": [
            {"title": "Мяч",
             "description": "Кожанный мяч"},
            {"title": "Коврик для йоги",
             "description": "Удобный коврик"},
            {"title": "Ракетка",
             "description": "Теннисная ракетка"}
        ],
        "Охота": [
            {"title": "Ружье",
             "description": "Охотничье ружье"},
            {"title": "Капкан",
             "description": "Капкан на медведя"},
            {"title": "Монок",
             "description": "Монок на кабана"}
        ],
        "Рыбалка": [
            {"title": "Удочка",
             "description": "Классическая удочка"},
            {"title": "Спининг",
             "description": "Прочный спининг"},
            {"title": "Блесна",
             "description": "Блесна ручной работы"}
        ],
        "Игрушки": [
            {"title": "Кукла",
             "description": "Красивая кукла"},
            {"title": "Машинка",
             "description": "Радиоуправляемая машинка"},
            {"title": "Мишка",
             "description": "Мягкий мишка"}
        ],
        "Развивающие": [
            {"title": "Пазл",
             "description": "Большие пазлы"},
            {"title": "Конструктор",
             "description": "Детский конструктор"},
            {"title": "Опыты",
             "description": "Набор для опытов"}
        ],
        "Детская гигиена": [
            {"title": "Подгузник",
             "description": "Удобный подгузник"},
            {"title": "Пеленка",
             "description": "Многоразовая пеленка"},
            {"title": "Присыпка",
             "description": "Детская присыпка"}
        ],
        "Мужская": [
            {"title": "Штаны",
             "description": "Удобные штаны"},
            {"title": "Рубашка",
             "description": "Белая рубашка"},
            {"title": "Костюм",
             "description": "Деловой костюм"}
        ],
        "Женская": [
            {"title": "Блузка",
             "description": "Модная блузка"},
            {"title": "Платье",
             "description": "Вечернее платье"},
            {"title": "Юбка",
             "description": "Длинная юбка"}
        ],
        "Детская": [
            {"title": "Ползунки",
             "description": "Удобные ползунки"},
            {"title": "Комбинезон",
             "description": "Практичный комбинезон"},
            {"title": "Детский Костюм",
             "description": "Костюм для утренника"}
        ],
    }

    discounts = [5, 10, 15, 20, 25, 50]

    root = Category.get_root_categories()
    for cat in root:
        subcats = Category.get_subcategories(cat.title)
        for subcat in subcats:
            items = products[subcat.title]
            for data in items:
                data["price"] = randint(1, 10) * 10
                if randint(0, 100) > 90:
                    discount = choice(discounts)
                else:
                    discount = 0
                data["discount"] = discount
                data["category"] = subcat
                Product.objects.create(**data)


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


def init_db(titles):
    init_text(titles)
    init_categories()
    init_products()
    put_pics()
    seed_attrs()


def drop_db(conn):
    conn.drop_database(db_name)


if __name__ == '__main__':
    db_name = 'webshop_db'
    connect = me.connect(db_name)

    init_db(TITLES)
    # drop_db(connect)
