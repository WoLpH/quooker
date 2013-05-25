import types
import re
from transform import Transform


class FloatTransform(Transform):
    '''Transformation to do string replacements of attribute values
    
    src -- The source attribute to get the data from, will be converted to unicode
    dst -- The destination attribute to set the data to
    pre_offset -- The offset to apply before the multiplier 
    multiplier -- The number to multiply the outcome with
    post_offset -- The offset to apply after the multiplier
    round -- Round to the given digits, None means no rounding 
    '''
    def __init__(self, src, dst=None, pre_offset=0, multiplier=1.,
            post_offset=0, round=None):
        if not dst:
            dst = src
        self.src, self.dst = src, dst
        self.pre_offset, self.post_offset = pre_offset, post_offset
        self.multiplier, self.round = multiplier, round

    def __call__(self, o):
        v = float(self.get(o, self.src, 0))
        v += self.pre_offset
        v *= self.multiplier
        v += self.post_offset
        if self.round:
            v = round(v, self.round)
        self.set(o, self.dst, v)
        return o

class LongTransform(Transform):
    '''Transformation to do string replacements of attribute values
    
    src -- The source attribute to get the data from, will be converted to unicode
    dst -- The destination attribute to set the data to
    pre_offset -- The offset to apply before the multiplier 
    multiplier -- The number to multiply the outcome with
    post_offset -- The offset to apply after the multiplier
    base -- The base to use, defaults to 10
    '''
    def __init__(self, src, dst=None, pre_offset=0, multiplier=1,
            post_offset=0, base=10):
        if not dst:
            dst = src
        self.src, self.dst = src, dst
        self.pre_offset, self.post_offset = pre_offset, post_offset
        self.multiplier, self.base = multiplier, base

    def __call__(self, o):
        v = self.get(o, self.src, 0)
        if self.base != 10:
            v = str(v)
            v = v[:v.find('.')]

        if isinstance(v, basestring):
            v = int(v, self.base)

        v += self.pre_offset
        v *= self.multiplier
        v += self.post_offset
        self.set(o, self.dst, v)
        return o

