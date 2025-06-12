from django import template

register = template.Library()

@register.filter(name='cap_every_word')
def cap_every_word(sentence):
    return " ".join([w.capitalize() for w in sentence.split(" ")])