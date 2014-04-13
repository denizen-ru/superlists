from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
import time


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        # inputbox.send_keys('testing' + Keys.ENTER)
        x = inputbox.location['x']
        width = inputbox.size['width']
        self.assertAlmostEqual(x + width / 2, 512, delta=6)
