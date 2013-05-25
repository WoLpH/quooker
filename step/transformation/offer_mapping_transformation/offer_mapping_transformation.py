
from transform import Transform
from quooker.step.transformation.name_split_transform import NameSplitTransform
from quooker.step.transformation.number_transform import *
from quooker.step.transformation.parse_price_transform import ParsePriceTransform


class OfferMappingTransform(Transform):
    '''
    
    Complex transformation, generating other transformations based
    on the available field mappings
    
    input_fields -- List with the columns mapped to input fields
    
    >>> from quooker.job.job import Job
    >>> row = dict(price='2.00', on_stock='Y', name='Philips xxx')
    >>> fields = [PriceInEuroField('price'), NameField('name'), StockField('on_stock')]
    >>> t = OfferMappingTransform(Job('test'), fields)
    >>> t(row)
    {'type': 'xxx', 'price': 2.0, 'on_stock': 'Y', 'name': 'Philips xxx', 'brand': 'Philips'}
    
    '''
    def __init__(self, input_fields):
        self.input_fields = input_fields
        self.initialize_transformations()
        
    def initialize_transformations(self):
        transformations = self.compute_transformations()
        self.transformations = transformations

    def compute_transformations(self):
        '''
        Based on the input fields, returns a list of transformations
        to execute
        '''
        field_dict = dict([(f.name, f) for f in self.input_fields])
        transformations = []
        if ('brand' not in field_dict or 'type' not in field_dict) and 'name' in field_dict:
            name_field = field_dict['name'].column
            transformations.append(NameSplitTransform(self.job, name_field, 'brand', 'type'))
        
        if 'price' in field_dict:
            price_column = field_dict['price'].column
            t = ParsePriceTransform(self.job, price_column, price_column)
            transformations.append(t)
            
        if 'price_cents' in field_dict:
            price_column = field_dict['price_cents'].column
            t = ParsePriceTransform(self.job, price_column, price_column)
            transformations.append(t)
            multiply = FloatTransform(self.job, price_column, price_column, multiplier=100)
            transformations.append(multiply)
            
        if 'stock' in field_dict:
            pass#on_stock_transformation        
        return transformations


    def __call__(self, row):
        
        for t in self.transformations:
            row = t(row)

        return row


#
#required_output_fields = ['product_name', 'type', 'brand', 'offer_price']
#
#    colors = models.TextField(null=True, blank=True)
#    materials = models.TextField(null=True, blank=True)
#    sizes = models.TextField(null=True, blank=True)
#
#    image_url = models.TextField(null=True, blank=True)
#    offer_price = models.IntegerField(null=True, blank=True)
#    offer_retailer_id = models.IntegerField()
#    category_id = models.IntegerField(null=True, blank=True)
#    retailer_product_id = models.CharField(max_length=255)
#    flag_updated = models.CharField(max_length=1)
#    ean = models.TextField(blank=True, null=True)
#    sku = models.TextField(blank=True, null=True)
#    offer_on_stock = models.CharField(blank=True, null=True, max_length=1)
#    offer_delivery_costs = models.IntegerField(null=True, blank=True)
#    offer_deeplink = models.TextField(null=True, blank=True)
#    entity_id = models.IntegerField(null=True, blank=True)
#    foreign_category = models.CharField(blank=True, null=True, max_length=255)
#    offer_delivery_time = models.CharField(blank=True, null=True, max_length=64)
#    is_active = models.BooleanField(null=True, blank=True, default=True)
#    match_author_id = models.IntegerField(null=True, blank=True) #zero is automatic 
#    match_set_at = models.DateTimeField(null=True, blank=True)
#    new_category_id = models.IntegerField(null=True, blank=True)
#    created_at = models.DateTimeField(null=True, blank=True)
#    match_score = models.FloatField(null=True, blank=True)
#    checked = models.BooleanField(default=False)
#    checked_at = models.DateTimeField(null=True, blank=True)
#    checked_by = models.IntegerField(null=True, blank=True)
#    sample_checked = models.BooleanField(default=False)
#    extra_text = models.TextField(null=True, blank=True)
#
#    #store the args to which the last entity was update
#    last_updated_entity_data = models.TextField(null=True, blank=True)
#    deactivated_at = models.DateTimeField(blank=True, null=True)
#


if __name__ == '__main__':
    from doctest import testmod
    testmod()


