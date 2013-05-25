from quooker.auto_configure.base_auto_configure import BaseAutoConfigure
from quooker.step.transformation.offer_mapping_transformation.input_fields import *
from framework.utils import parse_price
from decimal import InvalidOperation

class ColumnSample(object):
    def __init__(self, column, data_sample):
        self.column = column
        self.data_sample = data_sample
        self.meta = {}
        
        self.evaluate()
        
    def evaluate_url(self):
        is_url = False
        import re
        url = re.compile('.*\.[\w]{2,3}/')
        for row in self.data_sample:
            matches = url.match(row)
            if matches:
                return True
            
    def evaluate_description(self):
        is_description = False
        for row in self.data_sample:
            words = row.split(' ')
            if len(words) > 10:
                is_description = True
        return is_description
    
    def evaluate_numeric(self):
        numeric = False
        for row in self.data_sample:
            without_seperators = ''.join([x for x in unicode(row) if x not in [',', '.']])
            if without_seperators and without_seperators.isdigit():
                return True
    
    def evaluate_ean(self):
        for row in self.data_sample:
            clean = unicode(row).strip()
            if len(clean) == 13 and clean.isdigit():
                return True
        
                
        
    def evaluate_img(self):
        extensions = ['gif', 'jpg', 'jpeg', 'png']
        for row in self.data_sample:
            url = row.lower()
            for ext in extensions:
                if ext in url:
                    return True
        
    def evaluate_price_field(self):
        '''
        There has to be a dot or a comma in one of the prices
        '''
        is_price = False
        seperator_found = False
        total_price = 0
        for row in self.data_sample:
            if '.' in row or ',' in row:
                seperator_found = True
            try:
                price = parse_price(row)
                if price > 40000:
                    return False
                else:
                    total_price += price
                is_price = True
            except (ValueError,InvalidOperation), e:
                price = False
            if not price:
                return False
        is_price_field = is_price and seperator_found
        return is_price_field, total_price
        
    def evaluate(self):
        price_response = self.evaluate_price_field()
        if price_response:
            self.meta['price_field'], self.meta['total_price'] = price_response
        else:
            self.meta['price_field'], self.meta['total_price'] = None, None
        self.meta['image'] = self.evaluate_img()
        self.meta['url'] = self.evaluate_url()
        self.meta['description'] = self.evaluate_description()
        self.meta['numeric'] = self.evaluate_numeric()
        self.meta['ean'] = self.evaluate_ean()
        return self.meta
        

class ColumnAutoConfigure(BaseAutoConfigure):
    '''
    Given a sample of rows
    
    Determine which columns contain which data
    >>> from quooker.sample_data.feed_sample import feed_sample
    >>> c = ColumnAutoConfigure(feed_sample)
    >>> print c.auto_config()
    a
    '''

    def __init__(self, sample_rows):
        self.sample_rows = sample_rows
        
    def column_lists(self):
        from collections import defaultdict
        column_lists = defaultdict(list)
        for row in self.sample_rows:
            for k, v in dict(row).items():
                column_lists[k].append(v)
        return column_lists
    
    def column_samples(self):
        column_lists = self.column_lists()
        for k, values in column_lists.items():
            column_sample = ColumnSample(k, values)
            yield column_sample

    def auto_config(self):
        mappings = []
        unmapped = []
        column_samples = list(self.column_samples())
            
        #first find the price fields
        price_fields = [c for c in column_samples if c.meta['price_field']]
        price_fields.sort(key=lambda x: x.meta['total_price'], reverse=True)
        if price_fields:
            product_price = price_fields.pop()
            mappings.append(PriceInEuroField(product_price.column))
            column_samples.remove(product_price)
            if price_fields:
                delivery_costs = price_fields.pop()
                mappings.append(PriceInEuroField(delivery_costs.column))
                column_samples.remove(delivery_costs)

        image_fields = [c for c in column_samples if c.meta['image'] and c.meta['url']]
        if image_fields:
            pass#ImageField(product_price.column)

        unmapped = column_samples
        
        print mappings
        
    
    

if __name__ == '__main__':
    from doctest import testmod
    testmod()