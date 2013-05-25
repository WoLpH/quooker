import __builtin__
from transform import Transform

__all__ = ('CastTransform',)

class CastTransform(Transform):
    '''Transformation to do string replacements of attribute values
    
    src -- The source attribute to get the data from, will be converted to unicode
    dst -- The destination attribute to set the data to
    type -- Dunno dude 
    '''
    def __init__(self, src, dst, type):
        if not dst:
            dst = src
        self.src, self.dst = src, dst
        self.type = type

    def __call__(self, o):
        type_ = self.type
        if isinstance(type_, basestring):
            type_ = getattr(__builtin__, type_)

        self.set(o, self.dst, type_(self.get(o, self.src)))
        return o

