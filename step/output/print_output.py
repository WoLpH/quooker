from quooker.step.output.output import Output

class PrintOutput(Output):
    '''
    Simple output step for printing
    the resulting row
    
    >>> from quooker.job.job import Job
    >>> row = dict(name='Philips XS3')
    >>> t = PrintOutput()
    >>> t.set_job(Job('test'))
    >>> t(row)
    {'name': 'Philips XS3'}
    '''
    def __init__(self):
        pass
    
    def __call__(self, row):
        print row
    
if __name__ == '__main__':
    from doctest import testmod
    testmod()