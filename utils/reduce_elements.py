from functools import reduce

WHITE_LIST = ['p', 'b', 'strong', 'i', 'ul', 'ol', 'div', 'span']

def reduce_start_elements(elements):
     if (elements == '' or elements == None):
        raise ValueError("Input must be a list of elements, not an empty string")
     
     return reduce(
        lambda result, tag: result if tag.name not in WHITE_LIST else f'<{tag.name}>' + result,
        elements,
        ""
    )


def reduce_last_elements(elements):
     if (elements == '' or elements == None):
        raise ValueError("Input must be a list of elements, not an empty string")
     
     return reduce(
        lambda result, tag: result + f'</{tag.name}>' if tag.name in WHITE_LIST else result,
        elements,
        ""
    )