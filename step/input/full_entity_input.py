from input import Input
from tranquil import Session
from entity.alchemy_objects import FullProduct, FullCategory
from entity.alchemy_tables import entity_entity
from sqlalchemy import select, and_
from django.utils.functional import curry

ROWS_PER_BATCH = 1000

class FullProductCategoryInput(Input):
    def __init__(self, category_id, filters=None, session=None):
        if not session:
            session = Session()
        self.session = session

        self.category_id = category_id

        if not filters:
            filters = []
        filters.append(entity_entity.c.category_id == category_id)
        self.filters = filters

        self.results = session.execute(self.prepare_select())

    def set_category_id(self, category_id):
        self._category_id = category_id
        self._category = None

    def get_category_id(self):
        return self._category_id

    category_id = property(get_category_id, set_category_id)

    @property
    def category(self):
        if not self._category:
            self._category = FullCategory.get(self.category_id)
        return self._category

    def prepare_select(self):
        select_ = select(
            [entity_entity.c.id],
            and_(*self.filters),
            entity_entity,
            group_by=entity_entity.c.id,
        ).limit(10)
        return select_

    def flatten(self, item):
        flat = {}
        for value in item.values._values:
            print value

    def __iter__(self):
        get_many = curry(FullProduct.get_many,
            self.category_id,
            from_cache=True,
            session=self.session,
            category=self.category,
            ignore_errors=False,
            update_search=False,
            force_prime=True,
        )

        items = []
        for i, row in enumerate(self.results):
            if i and i % 1000 == 0:
                items = get_many(items)

                for item in items.itervalues():
                    yield self.flatten(item)

                items = []

            items.append(row.id)

        if items:
            items = get_many(items)

            for item in items.itervalues():
                yield self.flatten(item)

