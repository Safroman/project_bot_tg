

category_lookup = 'category'
root_lookup = 'root'
product_lookup = 'product'
separator = '_'
order_lookup = 'order'

cart_lookup = 'cart'
cart_plus = 'plus'
cart_minus = 'minus'
cart_remove = 'remove'
cart_checkout = 'checkout'

discount_lookup = 'discount'
back_lookup = ''

bot_map = {
    'Товары со скидкой': discount_lookup,
    category_lookup: 'category',
    cart_lookup: {
        cart_plus: 'plus',
        cart_minus: 'minus',
        cart_remove: 'remove',
        cart_checkout: 'checkout'
    }
}


def navigator(message=None, call=None):
    if message:
        data = [message.text, ]
    elif call:
        data = call.data.split(separator)

    var = bot_map

    for lookup in data:
        var = var[lookup]
        print(var)
    return var


if __name__ == '__main__':
    print(bot_map)
