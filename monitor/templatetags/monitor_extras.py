from django import template
register = template.Library()

@register.filter
def div( value, arg ):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = int( value )
        arg = int( arg )
        if arg: return value / arg
    except: pass
    return ''

@register.filter
def multiply( value, arg ):
    '''
    Multiplies the value; argument is the multiplier.
    Returns empty string on any error.
    '''
    try:
        value = int( value )
        arg = int( arg )
        if arg: return value * arg
    except: pass
    return ''
