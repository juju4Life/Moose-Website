from django import template

register = template.Library()


@register.simple_tag(name='dictionary')
def key_value(dictionary, key1, key2, key3, key4):

    return dictionary[key1][key2][key3][key4]


