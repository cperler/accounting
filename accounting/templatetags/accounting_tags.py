from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter(name='currency')
def currency(dollars):
    if dollars is None or dollars == '':
        dollars = 0.0
    dollars = round(float(dollars), 2)
    return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])

@register.filter(name='lookup')
def lookup(dct, index):
    try:
        if int(index) < len(dct):
            return dct[int(index)]
    except Exception:
        pass

    if index in dct:
        return dct[index]
    return ''

@register.assignment_tag
def cell(dct, col, row):
    return dct.get_cell(col, row)

@register.assignment_tag
def col_total(dct, col):
    return dct.get_col_total(col)