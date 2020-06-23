from models import Text, Category, Product
from random import randint, choice


def init_text():
    # Text.objects.create(
    #     title=Text.TITLES['greetings'],
    #     body='Рады приветствовать Вас в нашем интернет магазине'
    # )
    # Text.objects.create(
    #     title=Text.TITLES['cart'],
    #     body='Вы перешли в корзину'
    # )
    # Text.objects.create(
    #     title=Text.TITLES['categories'],
    #     body='В наличии есть такие категории'
    pass



    # subcategories = {
    #
    # }


subcategories = {
    "Продукты": ["Фрукты", "Овощи", "Напитки"],
    "Товары для дома": ["Хозяйственные товары", "Мебель", "Декор"],
    "Электроника": ["Кухонная техника", "Бытовая техника", "Компьютеры"],
    "Спорт и хобби": ["Спортивный инвентарь", "Охота", "Рыбалка"],
    "Детские товары": ["Игрушки", "Развивающие", "Детская гигиена"],
    "Одежда": ["Мужская", "Женская", "Детская"],
}

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

discount = [5, 10, 15, 20, 25, 50]





def init_products():
    root = Category.get_root_categories()
    for cat in root:
        subcats = Category.get_subcategories(cat.title)
        for subcat in subcats:
            items = products[subcat.title]
            for item in items:
                item["price"] = randint(1, 10) * 10
                item["discount"] = choice(discount)
                item["category"] = subcat
                Product.objects.create(**item)


if __name__ == '__main__':
    # init_text()
    # init_products()

    # for cat, d in subcategories.items():
    #     root = Category.objects.get(title=cat)
    #     subcategories = []
    #     for subcat_title in d:
    #         subcategory = Category.objects.get(title=subcat_title)
    #         subcategories.append(subcategory)
    #     root.subcategories = subcategories
    #     root.save()
    pass
