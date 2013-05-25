from transform import Transform


class StringFormatTransformation(Transform):
    '''Transformation to do string replacements of attribute values
    
    dst -- The destination attribute to set the data to
    format -- The format to use on the row
    
    >>> from quooker.job.job import Job
    >>> row = dict(a='right',c=2)
    >>> t = StringFormatTransformation(Job('test'), 'g', 'the result is %(a)s')
    >>> t(row)
    {'a': 'right', 'c': 2, 'g': 'the result is right'}
    
    '''
    def __init__(self, dst, format):
        self.dst = dst
        self.format = format

    def __call__(self, row):
        new_value = self.format % dict(row)

        self.set(row, self.dst, new_value)

        return row


if __name__ == '__main__':
    from doctest import testmod
    testmod()


