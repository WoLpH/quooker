import sys
import types

'Add all transformations to the transformations module'
module = __name__.rsplit('.', 1)[0]
transformations = sys.modules[module]

class TransformMeta(type):
    def __init__(cls, name, bases, dict):
        object_ = super(TransformMeta, cls).__init__(name, bases, dict)
        setattr(transformations, name, cls)


'''
TODO:
- Pickable configs
- Logging


'''


class Transform(object):
    '''The interface for a Transform object
    
    Must define a __call__(self, o) method
    
    >>> Transform()
    Traceback (most recent call last):
    ...
    NotImplementedError: Transform cannot be instantiated directly, it must be subclassed
    
    
    #TODO:
    error handling
    logging
    
    How to handle the addition of columns?
    How to change the set and get stuff
    List vs Dict
    
    '''

    __metaclass__ = TransformMeta

    def __init__(self):
        raise NotImplementedError, 'Transform cannot be instantiated directly, it must be subclassed'

    def set_job(self, job):
        self.job = job
        
    def start(self):
        '''
        Called just before the first row is send
        '''
        pass
        
    def finish(self):
        '''
        Called when the last row has been processed
        Or processing termines another way
        '''
        pass

    def __call__(self, row):
        '''
        Transforms the given row, usually a list
        Changes the data using set
        And returns the row
        '''
        raise NotImplementedError, '__call__ must be replaced with a working method'

    def get(self, *args, **kwargs):
        return self.job.get(*args, **kwargs)

    def set(self, *args, **kwargs):
        return self.job.set(*args, **kwargs)

