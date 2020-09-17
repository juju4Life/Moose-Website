
def template(cart):
    item_list = [
        f"{i.quantity}x {i.product.name} | {i.expansion} | {i.price} | {i.total}" for i in cart
    ]
    order = ""

    for item in cart:
        string = f"{item.product.name}<attribute>{item.expansion}<attribute>{item.product.printing}<attribute>near_mint<attribute>"

    return item_list

