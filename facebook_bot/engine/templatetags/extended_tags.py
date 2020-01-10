from django import template

register = template.Library()

@register.simple_tag(name='dictionary')
def keyvalue(dict, key1, key2, key3, key4):   
    print(key1) 
    print(key2) 
    print(key3) 
    print(key4) 
    return dict[key1][key2][key3][key4]


