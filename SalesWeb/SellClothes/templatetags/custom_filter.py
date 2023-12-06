from django import template  
import math  
register=template.Library()
@register.filter(name='currency')
def curency(number):
    if isinstance(number,int):
        return str(number)+"đ"
    else:
        return str(number)+"$"

@register.filter(name='multiply')
def multiply(number1,number2):
    return number1*number2

@register.simple_tag
def cal_sellprice(price , discount):
    if discount is None or discount is 0:
        return price
    sellprice = price
    sellprice = int(price - ( price * discount * 0.01 ))
    return math.floor(sellprice)

@register.simple_tag
def is_discount(discount):
    if discount!=0:
        return True;
    else:
        return False;

