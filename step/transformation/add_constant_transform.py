from transform import Transform


class AddConstantTransform(Transform):
    '''Transformation to do string replacements of attribute values
    
    dst -- The destination where to write the value
    value -- The constant value to add
    
    >>> from quooker.job.job import Job
    >>> row = dict(name='Philips XS3')
    >>> t = AddConstantTransform('a', 'b')
    >>> t.set_job(Job('test'))
    >>> t(row)
    {'a': 'b', 'name': 'Philips XS3'}
    
    '''
    def __init__(self, dst, value):
        self.dst = dst
        self.value = value

    def __call__(self, row):

        self.set(row, self.dst, self.value)

        return row


if __name__ == '__main__':
    from doctest import testmod
    testmod()


