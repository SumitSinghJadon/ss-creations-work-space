from django import template
import inflect
register = template.Library()


@register.simple_tag
def truncate_str(value, count, limit):
    if len(value) > count:
        return f"{value[:limit]}..."
    return value


@register.simple_tag
def sum_two_numbers(num1, num2):
    return num1 + num2


#@orion.hunter
@register.filter(name='trim_spaces')
def trim_spaces(value):
    if value:
        return value.strip()
    return value


@register.filter(name='number_to_text')
def number_to_text(value):
    p = inflect.engine()
    integer_part = int(value)
    decimal_part = value - integer_part

    if decimal_part > 0:
        text_integer_part = p.number_to_words(integer_part).title()
        text_decimal_part = p.number_to_words(decimal_part * 100).title()  # Convert decimal to a number between 0 and 100
        return f"{text_integer_part} and {text_decimal_part} percent"
    else:
        return p.number_to_words(integer_part).title()

@register.filter(name='convert_to_two_decimals')
def convert_to_two_decimals(value):
    if isinstance(value, float):
        return '{:.2f}'.format(value)
    return value

@register.filter(name='time_12h_format')
def time_12h_format(time_str):
    from datetime import datetime
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        time_12_hour_format = time_obj.strftime("%I:%M %p")
        return time_12_hour_format
    except ValueError:
        return time_str 
    
@register.filter(name='time_12h_format')
def time_12h_format(time_str):
    from datetime import datetime
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        time_12_hour_format = time_obj.strftime("%I:%M %p")
        return time_12_hour_format
    except ValueError:
        return time_str 
    
@register.filter(name='str_split')
def split_and_extract(value,index):
    tmp=value.split('-')
    return tmp[index]
