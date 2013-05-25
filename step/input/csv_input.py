from quooker.step.input.input import FileInput
import csv
import math
import os
import re

DELIMITERS = (',', '\t', ';', ':', '|', '~')
DELIMITER_STRING = re.escape(''.join(DELIMITERS))
NON_DELIMITER_RE = re.compile('[^%s]+' % DELIMITER_STRING, re.UNICODE)

'''Possible BOM (Byte Order Mark) encodings
It supports UTF-8, UTF-16 and UTF-32 both big and little endian

Don't change it to a dict, the order is important
'''

class Sniffer(object):
    def __init__(self, fh):
        self.fh = fh

    def detect(self, fh):
        original_position = fh.tell()
        delimiters = self.detect_delimiters()
        dialect = None

        '''Try to create a dialect for every character, the csv sniffer gets
        confused when many delimiters might be possible options'''
        for delimiter in delimiters:
            try:
                fh.seek(original_position)
                dialect = csv.Sniffer().sniff(fh.read(65536), delimiter)
                break
            except csv.Error:
                pass

        if not dialect:
            try:
                fh.seek(original_position)
                dialect = csv.Sniffer().sniff(fh.read(65536), DELIMITERS)
            except csv.Error:
                pass

        '''The Python csv module _only_ supports utf-8 and ascii so
        we must get rid of any unicode'''
        for k, v in dialect.__dict__.items():
            if isinstance(v, unicode):
                dialect.__dict__[k] = v.encode('utf-8')

        '''Return to the original position'''
        fh.seek(original_position)
        return dialect

    def detect_delimiters(self):
        '''Detect all possible delimiters and return the 5 most likely'''
        lines = []
        fh = self.fh
        original_position = fh.tell()
        fh.seek(0, 2)
        size = fh.tell()

        '''Read 4 lines from the begin of the file'''
        fh.seek(original_position)
        lines.append(fh.readline())
        lines.append(fh.readline())
        lines.append(fh.readline())
        lines.append(fh.readline())

        '''Read 4 lines from several parts of the file'''
        positions = (size / 4, size / 2, size / 4 * 2, size - 1000)
        for position in positions:
            fh.seek(position)
            fh.readline()
            lines.append(fh.readline())
            lines.append(fh.readline())
            lines.append(fh.readline())
            lines.append(fh.readline())

        '''Make sure we return the handle to it's original position'''
        fh.seek(original_position)

        '''Check which characters have the same occurance count for all lines
        This doesn't mean they have to be the same, it's just a guess'''
        charcounts = [c for l in lines for c in [self.get_charcount(l)] if c]
        chars = dict.fromkeys(''.join(''.join(c.keys()) for c in charcounts), 0)

        '''Calculate the distances from every item to every other item
        Basically we're building a 3 dimensional distance matrix while only
        storing the results
        '''
        for c in chars:
            for i in range(len(charcounts) - 1):
                for j in range(i + 1, len(charcounts)):
                    if i == j:
                        continue
                    elif charcounts[i].get(c, -i) == charcounts[j].get(c, -j):
                        chars[c] += 1

        '''Now the largest item in chars has the most similarity with the
        chars in the other lines. Since most chars here would be useless
        we will only return the top 5 chars'''

        chars = sorted(chars.iteritems(), key=lambda (k, v): (v, k))[:-6:-1]
        return (c for c, _ in chars)

    @classmethod
    def get_charcount(cls, string):
        '''Count the occurances of every character in the line with the
        exception of the linefeed and carriage return characters'''

        string = NON_DELIMITER_RE.sub('', string)
        return dict((c, string.count(c)) for c in set(string))

    @classmethod
    def sniff(cls, fh):
        sniffer = Sniffer(fh)
        return sniffer.detect(fh)

    @classmethod
    def has_headers(cls, fh):
        '''Detect if the file has headers'''
        original_position = fh.tell()

        '''Read 8KiB up to a newline to detect'''
        data = fh.read(8192).rsplit('\n', 1)[0]
        has_headers = csv.Sniffer().has_header(data)

        '''Return the filepointer to it's original position'''
        fh.seek(original_position)
        return has_headers

class CsvInput(FileInput):
    def __init__(self, job, filename, encoding=None, dialect=None,
            has_headers=None):
        FileInput.__init__(self, job, filename, encoding)
        self.reader = None
        self.encoding = None
        self.headers = None
        self.job = job
        self.set_filename(filename)
        self.set_encoding(encoding)
        self.set_dialect(dialect)
        self.set_has_headers(has_headers)

    def set_dialect(self, dialect):
        if not dialect:
            dialect = Sniffer.sniff(self.get_fh())
        self.dialect = dialect

    def set_has_headers(self, has_headers):
        if not has_headers:
            has_headers = Sniffer.has_headers(self.get_fh())
        self.has_headers = has_headers

    def get_reader(self):
        if not self.reader:
            fh = self.get_fh()
            if self.has_headers:
                headers = None
            else:
                reader = csv.reader(fh, self.dialect)
                items = reader.next()
                format_string = 'column_%%0%dd' % (math.log10(len(items)) + 1)
                headers = [format_string % i for i in range(1, len(items) + 1)]
                self.reset()

            self.reader = csv.DictReader(self.get_fh(), headers,
                dialect=self.dialect)
        return self.reader

    def __iter__(self):
        for row in self.get_reader():
            yield row

def utf8_encoder(fh):
    for line in fh:
        yield line.encode('utf-8')

if __name__ == '__main__':
    import glob
    import itertools
    import pprint
    base_path = os.path.abspath(os.path.join(__file__, '../../../'))
    samples = glob.glob(os.path.join(base_path, 'sample_data/*.csv'))
    for filename in samples:
        print 'Parsing: %s' % filename
        input = CsvInput(None, filename)
        for row in  itertools.islice(input, 2):
            pprint.pprint(row)

        print 'Delimiter: %r, Quote: %r, Example line:\n%s%s' % (
            input.dialect.delimiter, input.dialect.quotechar,
            input.fh.readline(), input.fh.readline()
        )
