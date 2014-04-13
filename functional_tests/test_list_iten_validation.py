from .base import FunctionalTest
from unittest import skip


class ItemValidationTest(FunctionalTest):

    # @skip('just skiping')
    def test_cannot_add_empty_list_items(self):
        self.fail('write me!')
