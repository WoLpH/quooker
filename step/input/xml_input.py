from cStringIO import StringIO
from lxml import etree
from quooker.step.input.input import FileInput
from collections import defaultdict
import os

SAMPLE_SIZE = 65536

class XMLDetector(object):
    def __init__(self, fh):
        self.fh = fh
    
    def get_tree(self):
        original_position = self.fh.tell()
        fh = StringIO(self.fh.read(SAMPLE_SIZE))
        self.fh.seek(original_position)
        fh.seek(0)
        tree = etree.iterparse(fh, remove_comments=True,
            remove_pis=True, remove_blank_text=True, events=('start', 'end'))
        return tree
    
    @classmethod
    def detect(cls, fh):
        self = XMLDetector(fh)
        tree = self.get_tree()
        tags = defaultdict(int)
        try:
            depth = 0
            for action, elem in tree:
                tag = elem.tag.split('}')[-1]
                
                has_text = str(bool(elem.text))
                if action == 'start':
                    depth += 1
                    if has_text:
                        tags[tag, depth] += 1
                elif action == 'end':
                    if has_text:
                        tags[tag, depth] += 1
                    depth -= 1
                else:
                    raise TypeError, 'unknown action %r' % action
        except etree.ParseError:
            pass
        
        tags = sorted(tags.iteritems(), key=lambda ((k, l), v): (l, v, k))
        average = sum(v for _, v in tags) / len(tags)
        main_tag = None
        main_depth = 0
        for (tag, depth), count in tags:
            if count > average:
                main_tag = tag
                main_depth = depth
                break
        tags = [(t, l) for (t, l), _ in tags if l > main_depth]
        
        return main_depth, main_tag, tags

class XMLInput(FileInput):
    def __init__(self, job, filename, main_depth=None, main_tag=None,
            tags=None, encoding=None):
        FileInput.__init__(self, job, filename, encoding)
        
        if not main_depth and not main_tag and not tags:
            main_depth, main_tag, tags = XMLDetector.detect(self.get_fh())
        self.main_depth = main_depth
        self.main_tag = main_tag
        self.tags = tags
    
    def get_tree(self):
        print self.get_fh().tell()
        tree = etree.iterparse(self.get_fh(), remove_comments=True,
            remove_pis=True, remove_blank_text=True,
            events=('start',))
        return tree
    
    def __iter__(self):
        tree = self.get_tree()
#        item = {}
#        for _, elem in tree:
#            tag = elem.tag.split('}')[-1]
#            if tag == self.main_tag:
#                if item:
#                    yield item
#                
#                item = {}
#            else:
#                text = elem.text
#                if text:
#                    item[tag] = text
    
        depth = 0
        item = {}
        for action, elem in tree:
            has_text = str(bool(elem.text))
            if action == 'start':
                depth += 1
            elif action == 'end':
                depth -= 1
                
            if elem.tag == self.main_tag and depth == self.main_depth:
                if item:
                    yield item
                item = {}
            elif depth > self.main_depth and has_text:
                item[elem.tag] = elem.text
            
        
        if item:
            yield item

if __name__ == '__main__':
    import glob
    import itertools
    import pprint
    base_path = os.path.abspath(os.path.join(__file__, '../../../'))
    samples = glob.glob(os.path.join(base_path, 'sample_data/*.xml'))
    for filename in samples:
        from framework.utils import timer
        t = timer()
        print 'Parsing: %s' % filename
        t.next()
        input = XMLInput(None, filename)
        print 'detecting filetype: %.6f' % t.next()
        
        print input.main_tag
        rows = 0
        #for row in itertools.islice(input, 100):
        for row in input:
            rows += 1
            #pprint.pprint(row)
            
        print 'parsing %d rows: %.6f' % (rows, t.next())
        print 'filesize:', os.path.getsize(filename)
        break
