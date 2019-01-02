"""
Question: https://stackoverflow.com/questions/53892450/get-the-format-in-dateutil-parse/53988718

Is there a way to get the "format" after parsing a date in dateutil. For example something like:

>>> x = parse("2014-01-01 00:12:12")
datetime.datetime(2014, 1, 1, 0, 12, 12)

x.get_original_string_format()
YYYY-MM-DD HH:MM:SS # %Y-%m-%d %H:%M:%S

# Or, passing the date-string directly
get_original_string_format("2014-01-01 00:12:12")
YYYY-MM-DD HH:MM:SS # %Y-%m-%d %H:%M:%S
"""

from datetime import datetime
import itertools
import re

FORMAT_CODES = (
    r'%a', r'%A', r'%w', r'%d', r'%b', r'%B', r'%m', r'%y', r'%Y',
    r'%H', r'%I', r'%p', r'%M', r'%S', r'%f', r'%z', r'%Z', r'%j',
    r'%U', r'%W',
)

TWO_LETTERS_FORMATS = (
    r'%p',
)

THREE_LETTERS_FORMATS = (
    r'%a', r'%b'
)

LONG_LETTERS_FORMATS = (
    r'%A', r'%B', r'%z', r'%Z',
)

SINGLE_DIGITS_FORMATS = (
    r'w',
)

TWO_DIGITS_FORMATS = (
    r'%d', r'%m', r'%y', r'%H', r'%I', r'%M', r'%S', r'%U', r'%W',
)

THREE_DIGITS_FORMATS = (
    r'%j',
)

FOUR_DIGITS_FORMATS = (
    r'%Y',
)

LONG_DIGITS_FORMATS = (
    r'%f',
)

# Non format code symbols
SYMBOLS = (
    '-',
    ':',
    '+',
    'Z',
    ',',
    ' ',
    '.'
)


if __name__ == '__main__':
    date_str = input('Please input a date: ')

    # Split with non format code symbols
    pattern = r'[^{}]+'.format(''.join(SYMBOLS))
    components = re.findall(pattern, date_str)

    # Create a format placeholder, eg. '{}-{}-{} {}:{}:{}+{}'
    placeholder = re.sub(pattern, '{}', date_str)

    formats = []
    for comp in components:
        if re.match(r'^\d{1}$', comp):
            formats.append(SINGLE_DIGITS_FORMATS)
        elif re.match(r'^\d{2}$', comp):
            formats.append(TWO_DIGITS_FORMATS)
        elif re.match(r'^\d{3}$', comp):
            formats.append(THREE_DIGITS_FORMATS)
        elif re.match(r'^\d{4}$', comp):
            formats.append(FOUR_DIGITS_FORMATS)
        elif re.match(r'^\d{5,}$', comp):
            formats.append(LONG_DIGITS_FORMATS)
        elif re.match(r'^[a-zA-Z]{2}$', comp):
            formats.append(TWO_LETTERS_FORMATS)
        elif re.match(r'^[a-zA-Z]{3}$', comp):
            formats.append(THREE_LETTERS_FORMATS)
        elif re.match(r'^[a-zA-Z]{4,}$', comp):
            formats.append(LONG_LETTERS_FORMATS)
        else:
            formats.append(FORMAT_CODES)

    # Create a possible format set
    possible_set = itertools.product(*formats)

    found = 0
    for possible_format in possible_set:
        # Create a format with possible format combination
        dt_format = placeholder.format(*possible_format)
        try:
            dt = datetime.strptime(date_str, dt_format)
            # Use the format to parse the date, and format the
            # date back to string and compare with the origin one
            if dt.strftime(dt_format) == date_str:
                print('Possible date format: {}'.format(dt_format))
                found += 1
        except Exception:
            continue

    if found == 0:
        print('No pattern found')
