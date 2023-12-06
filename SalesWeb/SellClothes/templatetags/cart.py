from django import template    
register=template.Library()
@register.filter(name='is_in_cart')
def is_in_cart(product ,cart):
    keys=cart.keys()
    for id in keys:
        if int(id)== product.id:
            return True
    return False;
@register.filter(name='cart_quantity')
def cart_quantity(product ,cart):
    keys=cart.keys()
    for id in keys:
        if int(id)== product.id:
            return cart.get(id)
    return 0

@register.filter(name='price_total')
def price_total(product ,cart):
    discount=product.discount
    if discount!=0:
        sellprice = int(product.price - ( product.price * discount * 0.01 ))
        return sellprice*cart_quantity(product , cart)
    return product.price * cart_quantity(product , cart)

@register.filter(name='total_cart_price')
def total_cart_price(products , cart):
    sum=0;
    for p in products:
        sum+=price_total(p ,cart)
    return sum

@register.filter(name='convert_USD')
def convert_USD(products, cart):
    x=total_cart_price(products,cart)
    x=x/23500
    return round(x,2)

@register.simple_tag
def convert(products, cart):
    x=total_cart_price(products,cart)
    x=x/23500
    return round(x,2)

@register.filter(name='is_price')
def is_price(products , cart):
    sum=0;
    for p in products:
        sum+=price_total(p ,cart)
    if sum ==0:
        return False
    else :
        return True


