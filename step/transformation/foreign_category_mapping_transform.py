from transform import Transform


class ForeignCategoryMappingTransform(Transform):
    '''Transformation to map foreign categories
    
    >>> from quooker.job.job import Job
    >>> row = dict(foreign_category='Televisies')
    >>> t = ForeignCategoryMappingTransform(0)
    >>> t.set_job(Job('test'))
    >>> t(row)
    {'foreign_category': 'Televisies', 'category_id': 100}
    
    '''
    def __init__(self, retailer_id, src='foreign_category', dst='category_id', default_category_id=100):
        self.src = src
        self.dst = dst
        self.retailer_id = retailer_id
        self.default_category_id = default_category_id
        
        self.mapping_dict = {}
        self.new_foreign_categories = []
        
    def start(self):
        '''
        Load the mapping data
        '''
        pass
        
    def finish(self):
        '''
        Actually send all the data (new_foreign_categories) to
        the mapping database
        '''
        pass
        

    def __call__(self, row):
        foreign_category = self.get(row, self.src)
        category_id = self.mapping_dict.get(foreign_category)
        
        if not category_id:
            #create the foreign category
            self.mapping_dict[foreign_category] = category_id = self.default_category_id
            self.new_foreign_categories.append(foreign_category)
            
        self.set(row, self.dst, category_id)
        
        return row


if __name__ == '__main__':
    from doctest import testmod
    testmod()


