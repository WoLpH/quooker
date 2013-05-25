from django.core.management.base import BaseCommand

from data_import.transformations import *
from data_import.inputs.full_entity_input import FullProductCategoryInput

class Command(BaseCommand):
    #can_import_settings = True
    #requires_model_validation = True

    def handle(self, *args, **kwargs):
        print 'args: %s\nkwargs: %s' % (args, kwargs)

        entities = FullProductCategoryInput(12)
        for entity in entities:
            print entity
        return

        entity = dict(foo='bar', spam='eggs', test='12345')
        entities = [dict(foo='bar', spam='eggs', test='12345'), dict(foo='bar', spam='eggs', test='12345')]


        print entity
        transformations = []

        transformations.append(StringReplaceTransform(
            src='foo',
            dst='foo',
            search='bar',
            replace='jeuj',
            regex=False,
        ))

        transformations.append(StringReplaceTransform(
            src='spam',
            dst='eggs',
            search='eggs',
            replace='basket',
            regex=False,
        ))

        transformations.append(FloatTransform('test', multiplier=2.5))
        transformations.append(LongTransform('test', multiplier=10e32, base=9))
        transformations.append(CastTransform('spam', 'unispam', unicode))

        print reduce(lambda x, y: y(x), transformations, entity)
