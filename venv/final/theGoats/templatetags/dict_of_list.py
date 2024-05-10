from django.template.defaultfilters import register

@register.filter(name='dict_of_list')
def dict_of_list(l, i):
    '''Returns the list item at index i.'''
    return l[i]