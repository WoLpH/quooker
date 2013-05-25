from transform import Transform


class NameSplitTransform(Transform):
    '''Transformation to do string replacements of attribute values
    
    src -- The field containing the name
    dst -- The destination attribute to set the brand to
    dst_type -- The destination to write the type to
    
    >>> from quooker.job.job import Job
    >>> row = dict(name='Philips XS3')
    >>> t = NameSplitTransform(Job('test'), 'name', 'brand', 'type')
    >>> t(row)
    {'brand': 'Philips', 'type': 'XS3', 'name': 'Philips XS3'}
    
    '''
    def __init__(self, src, dst, dst_type):
        self.src = src
        self.dst = dst
        self.dst_type = dst_type

    def __call__(self, row):
        value = self.get(row, self.src)
        if ' ' in value:
            brand, type = value.split(' ', 1)
        else:
            brand = value
            type = ''

        self.set(row, self.dst, brand)
        self.set(row, self.dst_type, type)

        return row


if __name__ == '__main__':
    from doctest import testmod
    testmod()


