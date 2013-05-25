import codecs
import os
import sys

'Add all inputs to the inputs module'
module = __name__.rsplit('.', 1)[0]
inputs = sys.modules[module]

ENCODINGS = (
    (codecs.BOM_UTF32_LE, 'utf-32-le'),
    (codecs.BOM_UTF32_BE, 'utf-32-be'),
    (codecs.BOM_UTF16_LE, 'utf-16-le'),
    (codecs.BOM_UTF16_BE, 'utf-16-be'),
    (codecs.BOM_UTF8, 'utf-8'),
)

DEFAULT_ENCODING = 'utf-8'

def detect_encoding(filename):
    '''Open a file with the given encoding or autodetect

    Detection works by reading the BOM headers in the file (if available)
    and defaults to utf-8 if no encoding matches'''
    fh = open(filename)
    bom = fh.read(4)
    fh.close()

    offset = 0
    for BOM, encoding in ENCODINGS:
        if bom.startswith(BOM):
            offset = len(BOM)
            break

    if not encoding:
        offset = 0
        encoding = DEFAULT_ENCODING

    return offset, encoding

class InputMeta(type):
    def __init__(cls, name, bases, dict):
        super(InputMeta, cls).__init__(name, bases, dict)
        setattr(inputs, name, cls)

class Input(object):
    '''The interface for a Input object
    
    Must define an iteration method (e.g. __iter__ or __getitem__)
    
    >>> Input()
    Traceback (most recent call last):
    ...
    NotImplementedError: Input cannot be instantiated directly, it must be subclassed
    '''

    __metaclass__ = InputMeta

    def __init__(self, job):
        raise NotImplementedError, 'Input cannot be instantiated directly, it must be subclassed'

    def __iter__(self):
        #yield the list items
        raise NotImplementedError, 'Input classes must implement an iter method'

class FileInput(Input):
    def __init__(self, job, filename, encoding=None):
        self.offset = 0
        self.fh = None
        self.encoding = None
        self.set_filename(filename)
        self.set_encoding(encoding)

    def set_filename(self, filename):
        if self.fh:
            self.fh.close()
            self.fh = None

        filename = os.path.abspath(filename)
        assert os.path.isfile(filename)
        self.filename = filename

    def set_encoding(self, encoding):
        if not encoding:
            offset, encoding = detect_encoding(self.filename)
            self.offset = offset
        self.encoding = encoding

    def get_fh(self):
        if not self.fh:
            self.fh = codecs.EncodedFile(
                codecs.open(self.filename, encoding=self.encoding), 'utf-8')
            self.fh.seek(self.offset)
        return self.fh

    def reset(self):
        self.get_fh().seek(self.offset)
