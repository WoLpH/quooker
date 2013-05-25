

class RowHandler(object):
    pass

class DictRowHandler(RowHandler):
    @classmethod
    def get(self, row, k, default=None):
        return row.get(k, default)

    @classmethod
    def set(self, row, k, v):
        row[k] = v


class Job(object):
    '''
    Main object responsible for all transformations under it
    

    '''
    def __init__(self, name, steps = False, row_handler=None):
        self.name = name
        self.steps = steps or []

        if not row_handler:
            self.row_handler = DictRowHandler
        else:
            self.row_handler = row_handler
            
        self.get = self.row_handler.get
        self.set = self.row_handler.set

#    def get(self, *args, **kwargs):
#        return self.row_handler.get(*args, **kwargs)
#    
#    def set(self, *args, **kwargs):
#        return self.row_handler.set(*args, **kwargs)
    
    def prepend_steps(self):
        return []
    
    def append_steps(self):
        return []
    
    def all_steps(self):
        return self.prepend_steps() + self.steps + self.append_steps()
    
    def execute(self, input, test=False):
        
        #prepare all steps
        steps = []
        for s in self.all_steps():
            s.set_job(self)
            steps.append(s)
        
        [s.start() for s in steps]
        try:
            for row in input:
                yield reduce(lambda x, y: y(x), steps, row)
        except:
            [s.finish() for s in steps]
        #signal we're done
        
        
#            for s in steps:
#                row = s(row)
#            if test:
#                yield row


class OfferJob(Job):
    '''
    Job with predefined behaviour for offers
    
    >>> j = OfferJob('offer_example_job_bol', 46)
    >>> sample = [{'a': 'b'}]
    >>> result_iterator = j.execute(sample, test=True)
    >>> list(result_iterator)
    [{'a': 'b', 'offer_retailer_id': 46, 'category_id': 100, 'flag_updated': 'Y'}]
    '''
    def __init__(self, name, retailer_id, row_handler=None):
        self.retailer_id = retailer_id
        Job.__init__(self, name, row_handler=row_handler)
    
    
    def prepend_steps(self):
        return []
    
    def append_steps(self):
        transformations = []

        from quooker.step.transformation.foreign_category_mapping_transform import ForeignCategoryMappingTransform
        from quooker.step.transformation.add_constant_transform import AddConstantTransform
        updated = AddConstantTransform('flag_updated', 'Y')
        transformations.append(updated)
        retailer = AddConstantTransform('offer_retailer_id', self.retailer_id)
        transformations.append(retailer)
        category_mapping = ForeignCategoryMappingTransform(self.retailer_id)
        transformations.append(category_mapping)
        
        return transformations
        
        
    
if __name__ == '__main__':
    from doctest import testmod
    testmod()

    
    



