from transform import Transform
from framework.utils import parse_price


class ParsePriceTransform(Transform):
    '''Transformation to do string replacements of attribute values
    
    src -- The source attribute to get the data from, will be converted to unicode
    dst -- The destination attribute to set the data to
    decimal_separator -- Optional
    thousand_separator -- Optional
    
    >>> from quooker.job.job import Job
    >>> row = dict(price='25.25',c=2)
    >>> t = ParsePriceTransform(Job('test'), 'price', 'price')
    >>> t(row)
    {'c': 2, 'price': 25.25}
    
    '''
    def __init__(self, src, dst, decimal_separator=None, thousand_separator=None):
        self.src = src
        self.dst = dst
        self.decimal_separator = decimal_separator
        self.thousand_separator = thousand_separator

    def __call__(self, row):
        value = self.get(row, self.src)
        new_value = parse_price(value, self.decimal_separator, self.thousand_separator)

        self.set(row, self.dst, new_value)

        return row



if __name__ == '__main__':
    from doctest import testmod
    testmod()
