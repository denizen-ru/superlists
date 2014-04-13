from .base import FunctionalTest
from unittest import skip, Keys


class ItemValidationTest(FunctionalTest):

    # @skip('just skiping')
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element_by_id(
            'id_new_item').send_keys('Buy milk' + Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')

        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element_by_id(
            'id_new_item').send_keys('Make tea' + Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: MAke tea')