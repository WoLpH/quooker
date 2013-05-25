
class InputField(object):
    def __init__(self, column):
        self.column = column


class UrlField(InputField):
    name = 'url'
    
class Deeplink(UrlField):
    name = 'deeplink'
    
class ImageUrl(UrlField):
    name = 'image_url'

class NameField(InputField):
    name = 'name'

class BrandField(InputField):
    name = 'brand'

class TypeField(InputField):
    name = 'type'

class PriceInEuroField(InputField):
    name = 'price'

class PriceInEuroCentsField(InputField):
    name = 'price_cents'

class StockField(InputField):
    name = 'stock'
    def __init__(self, column, true_values=None, false_values=None):
        self.column = column
        self.true_values = true_values
        self.false_values = false_values
