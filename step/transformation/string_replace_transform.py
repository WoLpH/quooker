import types
import re
from transform import Transform

__all__ = ('StringReplaceTransform',)

class StringReplaceTransform(Transform):
    '''Transformation to do string replacements of attribute values
    
    src -- The source attribute to get the data from, will be converted to unicode
    dst -- The destination attribute to set the data to
    search -- The search string or list of strings
    replace -- The replacement string or list of strings
    regex -- This flag can be an integer (e.g. re.IGNORECASE) or True to enable regular expressions
    '''
    def __init__(self, src, dst, search, replace, regex=False):
        if not isinstance(search, types.ListType):
            search = [search]
            replace = [replace]
        elif not isinstance(search, types.ListType) and \
                len(search) != len(replace) and len(replace) == 1:
            replace = replace * len(search)

        if regex:
            if regex is not True and isinstance(regex, int):
                print 'regex is int?', regex
                flags = regex
            else:
                flags = 0
            search = [re.compile(s, flags) for s in search]

        self.src, self.dst, self.replace, self.regex, self.search = src, dst, replace, regex, search

    def __call__(self, o):
        v = self.get(o, self.src, '')
        if self.regex:
            for k, s in enumerate(self.search):
                v = s.sub(self.replace[k], v)
        else:
            for k, s in enumerate(self.search):
                v = v.replace(s, self.replace[k])
        self.set(o, self.dst, v)
        return o
